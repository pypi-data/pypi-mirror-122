import logging
import time
from typing import Callable

import storm_scheduler
from storm_scheduler import exception

LOG = logging.getLogger(__name__)


class Task:
    def __init__(self, func, *args, **kwargs):
        if not isinstance(func, Callable):
            raise exception.TaskError('Task function needs to be callable')
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._interval = None
        self._next_run = None
        self.last_runtime = None

    def __str__(self):
        if not self._interval:
            return f'<Task: {self._func.__name__} not yet scheduled to run>'
        return f'<Task: {self._func.__name__} scheduled to run every {self._interval}s>'

    def every(self, value, unit='seconds'):
        """Run a task every X units! (e.g. every 30 seconds)

        :param int,float value: Interval
        :param str unit: Time unit (e.g. seconds, minutes, hours, days)
        :raises TaskError: This is raised when there is an issue with the Task.
        """
        if not isinstance(value, (int, float)):
            raise exception.TaskError('Task interval needs to be an integer or float')
        elif value <= 0:
            raise exception.TaskError('Interval cannot be zero or negative')
        elif unit not in storm_scheduler.ALLOWED_TIME_UNITS:
            raise exception.TaskError(f"Unit '{unit}' not in the list of supported time units")

        unit = str(unit).lower()
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
