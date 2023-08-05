import logging
import time

import storm_scheduler
from storm_scheduler import exception

LOG = logging.getLogger(__name__)


class Task:
    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._interval = None
        self._next_run = None
        self.last_runtime = None

    def __str__(self):
        return f'<Task: {self._func.__name__} schedule to run in {round(max(self.next_run, 0), 3)}s>'

    def every(self, value, unit='seconds'):
        """Run a task every X units! (e.g. every 30 seconds)

        :param int,float value: Value
        :param str unit: Time unit (e.g. seconds, minutes, hours, days)
        """
        unit = unit.lower()
        seconds = value
        if unit == storm_scheduler.MINUTES:
            seconds += seconds * 60
        elif unit == storm_scheduler.HOURS:
            seconds += seconds * 60 * 60
        elif unit == storm_scheduler.DAYS:
            seconds += seconds * 60 * 60 * 60

        self._interval = seconds
        self._next_run = time.monotonic() + self._interval

        return self

    def run(self):
        """Execute the Task."""
        start_time = time.monotonic()

        try:
            self._func(*self._args, **self._kwargs)
        except exception.TaskError as why:
            LOG.warning(f'Task Error: {why}')
        finally:
            self.last_runtime = time.monotonic() - start_time
            interval = max(self._interval - self.last_runtime, 0.01)
            self._next_run = time.monotonic() + interval

    @property
    def should_run(self):
        """Are we ready to run again?"""
        return self.next_run <= 0

    @property
    def next_run(self):
        """Time remaining until next run."""
        return self._next_run - time.monotonic()
