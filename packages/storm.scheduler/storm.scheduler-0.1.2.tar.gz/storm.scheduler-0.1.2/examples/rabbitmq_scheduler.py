import logging
import time

import amqpstorm
import storm_scheduler
from storm_scheduler import exception

logging.basicConfig(level=logging.DEBUG)

LOG = logging.getLogger(__name__)


class MyService:
    def __init__(self):
        self.schedule = storm_scheduler.Scheduler()

        # RabbitMQ Connection
        self.connection = amqpstorm.Connection('localhost', 'guest', 'guest')
        self.channel = self.connection.channel()
        self.channel.queue.declare('storm.scheduler.messages')

        # Schedule some recurring tasks.
        self.schedule.task(self.hello_world, 'Hello World').every(3)
        self.schedule.task(self.stop_scheduler, message='Shutting down').every(1, 'minutes')

    def hello_world(self, message):
        msg = f'{message} {int(time.time())}'

        message = amqpstorm.Message.create(self.channel, msg)
        message.publish('storm.scheduler.messages')

        LOG.info(msg)

    def stop_scheduler(self, message='Default'):
        msg = f"{message}: It wasn't my time"

        message = amqpstorm.Message.create(self.channel, msg)
        message.publish('storm.scheduler.messages')

        self.channel.close()
        self.connection.close()

        raise exception.AbortScheduler(msg)


if __name__ == '__main__':
    SERVICE = MyService()
    SERVICE.schedule.loop()
