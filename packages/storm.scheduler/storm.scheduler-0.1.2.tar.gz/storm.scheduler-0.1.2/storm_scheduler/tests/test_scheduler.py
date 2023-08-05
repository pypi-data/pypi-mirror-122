import threading
import time
import unittest

from storm_scheduler import scheduler
from storm_scheduler import exception


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

    def test_task_interval_too_low(self):
        schedule = scheduler.Scheduler()
        schedule.set_state(schedule.OPEN)

        task = schedule.task(lambda: None)

        self.assertRaisesRegex(
            exception.TaskError,
            'Interval cannot be zero or negative',
            task.every, -0.01,
        )

        self.assertRaisesRegex(
            exception.TaskError,
            'Interval cannot be zero or negative',
            task.every, 0,
        )

    def test_task_time_unit_not_supported(self):
        schedule = scheduler.Scheduler()
        schedule.set_state(schedule.OPEN)

        task = schedule.task(lambda: None)

        self.assertRaisesRegex(
            exception.TaskError,
            "Unit 'second' not in the list of supported time units",
            task.every, 1, 'second'
        )

        self.assertRaisesRegex(
            exception.TaskError,
            "Unit 'None' not in the list of supported time units",
            task.every, 1, None
        )

    def test_task_interval_invalid(self):
        schedule = scheduler.Scheduler()
        schedule.set_state(schedule.OPEN)

        task = schedule.task(lambda: None)

        self.assertRaisesRegex(
            exception.TaskError,
            'Task interval needs to be an integer or float',
            task.every, "don't allow strings"
        )

        self.assertRaisesRegex(
            exception.TaskError,
            'Task interval needs to be an integer or float',
            task.every, None
        )

    def test_task_function_invalid(self):
        schedule = scheduler.Scheduler()

        self.assertRaisesRegex(
            exception.TaskError,
            'Task function needs to be callable',
            schedule.task, "don't allow strings"
        )

        self.assertRaisesRegex(
            exception.TaskError,
            'Task function needs to be callable',
            schedule.task, None
        )

        self.assertRaisesRegex(
            exception.TaskError,
            'Task function needs to be callable',
            schedule.task, 1
        )

    def test_string_representation(self):
        schedule = scheduler.Scheduler()
        schedule.set_state(schedule.OPEN)

        def hello_world():
            pass

        task1 = schedule.task(hello_world).every(0.01)
        task2 = schedule.task(hello_world).every(6)
        task3 = schedule.task(hello_world).every(9)

        self.assertEqual('<Task: hello_world scheduled to run every 0.01s>', str(task1))
        self.assertEqual('<Task: hello_world scheduled to run every 6s>', str(task2))
        self.assertEqual('<Task: hello_world scheduled to run every 9s>', str(task3))

    def test_string_representation_without_interval_set(self):
        schedule = scheduler.Scheduler()
        schedule.set_state(schedule.OPEN)

        def hello_world():
            pass

        task = schedule.task(hello_world)

        self.assertEqual('<Task: hello_world not yet scheduled to run>', str(task))
