import logging
import time

from storm_scheduler import base
from storm_scheduler import exception
from storm_scheduler.task import Task

LOG = logging.getLogger(__name__)

MIN_IDLE_TIME = 0.01
MAX_IDLE_TIME = 1.0


class Scheduler(base.Stateful):
    def __init__(self, on_error=None):
        super(Scheduler, self).__init__()
        self._on_error = on_error
        self._tasks = []

    def loop(self):
        """Scheduler loop."""
        self.set_state(self.OPEN)
        while self.is_open:
            self._loop()
            time.sleep(self._idle_wait())
        self.set_state(self.CLOSED)

    def stop(self):
        """Stop the scheduler."""
        self.set_state(self.CLOSED)

    def task(self, func, *arg, **kwargs):
        """Create a scheduler task."""
        task = Task(func, *arg, **kwargs)
        self._tasks.append(task)
        return task

    def _handle_task_error(self, task, why):
        try:
            self._on_error(why)
        except exception.CancelTask as why:
            LOG.warning(f'Cancelled Task: {why}')
            self._tasks.remove(task)
        except exception.AbortScheduler as why:
            LOG.warning(f'Stopping Scheduler: {why}')
            self.set_state(self.CLOSING)

    def _idle_wait(self):
        if not self.is_open:
            return 0
        max_wait = None
        for task in self._tasks:
            remaining = task.next_run
            if max_wait is None or max_wait > remaining:
                max_wait = remaining
        return min(max(max_wait, MIN_IDLE_TIME), MAX_IDLE_TIME)

    def _loop(self):
        for task in self._tasks:
            if self.is_closed:
                break
            elif not task.should_run:
                continue
            try:
                task.run()
            except exception.CancelTask as why:
                LOG.warning(f'Cancelled Task: {why}')
                self._tasks.remove(task)
            except exception.AbortScheduler as why:
                LOG.warning(f'Stopping Scheduler: {why}')
                self.set_state(self.CLOSING)
                break
            except Exception as why:
                LOG.exception(f'Unexpected Task Error: {why}')
                if self._on_error is not None:
                    self._handle_task_error(task, why)
                break
