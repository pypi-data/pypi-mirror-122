"""Storm-Scheduler"""
__version__ = '0.1.1'  # noqa
__author__ = 'eandersson'  # noqa

from storm_scheduler.exception import AbortScheduler  # noqa
from storm_scheduler.exception import CancelTask  # noqa
from storm_scheduler.exception import SchedulerError  # noqa
from storm_scheduler.exception import TaskError  # noqa
from storm_scheduler.scheduler import Scheduler  # noqa

SECONDS = 'seconds'
MINUTES = 'minutes'
HOURS = 'hours'
DAYS = 'days'
