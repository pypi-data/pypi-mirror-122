import threading
import time
import unittest

from storm_scheduler import scheduler


class TestScheduler(unittest.TestCase):
    def test_schedule_task(self):
        schedule = scheduler.Scheduler()

        self.call_count = 0

        def hello_world():
            self.call_count += 1

        # Stop the scheduler after 1 second.
        timer = threading.Timer(1.0, lambda: schedule.stop())
        timer.start()

        # Schedule a task to run every 0.3 seconds.
        schedule.task(hello_world).every(0.3)

        # Start loop.
        schedule.loop()

        # Make sure we called hello_world 3 three times.
        self.assertEqual(3, self.call_count)

    def test_schedule_task_with_arguments(self):
        schedule = scheduler.Scheduler()

        self.call_count = 0
        self.results = None

        def hello_world(hello, message=None):
            self.call_count += 1
            self.results = f'{hello} {message}'

        # Stop the scheduler after 1 second.
        timer = threading.Timer(1.0, lambda: schedule.stop())
        timer.start()

        # Schedule a task to run every 0.5 seconds.
        schedule.task(hello_world, 'hello', message='world').every(0.5)

        # Start loop.
        schedule.loop()

        # Make sure we called it at least once.
        self.assertEqual(1, self.call_count)
        self.assertIsNotNone(self.results)
        self.assertEqual('hello world', self.results)

    def test_idle_wait(self):
        schedule = scheduler.Scheduler()
        schedule.set_state(schedule.OPEN)

        task1 = schedule.task(lambda: None).every(0.01)
        task2 = schedule.task(lambda: None).every(2)
        task3 = schedule.task(lambda: None).every(3)

        time.sleep(0.01)

        schedule._loop()

        self.assertEqual(0.01, schedule._idle_wait())
        self.assertIsNotNone(task1._next_run)
        self.assertGreaterEqual(1, int(task2.next_run))
        self.assertGreaterEqual(2, int(task3.next_run))

    def test_string_representation(self):
        schedule = scheduler.Scheduler()
        schedule.set_state(schedule.OPEN)

        def hello_world():
            pass

        task1 = schedule.task(hello_world).every(3)
        task2 = schedule.task(hello_world).every(6)
        task3 = schedule.task(hello_world).every(9)

        self.assertEqual('<Task: hello_world schedule to run in 3.0s>', str(task1))
        self.assertEqual('<Task: hello_world schedule to run in 6.0s>', str(task2))
        self.assertEqual('<Task: hello_world schedule to run in 9.0s>', str(task3))
