class SchedulerError(Exception):
    """Generic Scheduler error."""
    pass


class AbortScheduler(SchedulerError):
    """Stop the scheduler."""
    pass


class TaskError(SchedulerError):
    """Generic task error. This will log, but not stop the task."""
    pass


class CancelTask(SchedulerError):
    """Permanently cancel the task."""
    pass
