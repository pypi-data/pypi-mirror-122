import logging
import time

import storm_scheduler
from storm_scheduler import exception

logging.basicConfig(level=logging.DEBUG)

LOG = logging.getLogger(__name__)


class MyService:
    def __init__(self):
        self.schedule = storm_scheduler.Scheduler()

        # Schedule some recurring tasks.
        self.schedule.task(self.hello_world, 'Hello World').every(3)
        self.schedule.task(self.stop_scheduler, message='Shutting down').every(1, 'minutes')

    def hello_world(self, message):
        LOG.info(f'{message} {int(time.time())}')

    def stop_scheduler(self, message='Default'):
        raise exception.AbortScheduler(f"{message}: It wasn't my time")


if __name__ == '__main__':
    SERVICE = MyService()
    SERVICE.schedule.loop()
