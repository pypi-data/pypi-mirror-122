import logging
import time

import storm_scheduler
from storm_scheduler import exception

logging.basicConfig(level=logging.DEBUG)

LOG = logging.getLogger(__name__)


def hello_world():
    LOG.info(f'Hello World {int(time.time())}')


def stop_scheduler():
    raise exception.AbortScheduler("It wasn't my time")


if __name__ == '__main__':
    SCHEDULE = storm_scheduler.Scheduler()
    SCHEDULE.task(hello_world).every(3)
    SCHEDULE.task(stop_scheduler).every(1, 'minutes')
    SCHEDULE.loop()
