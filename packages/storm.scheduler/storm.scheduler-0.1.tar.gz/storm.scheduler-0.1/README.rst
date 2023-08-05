Storm.Scheduler
===============
A simple task scheduling library.

.. code-block:: shell

    pip install storm.scheduler

Example usage
-------------
A simple example would look like this.

.. code:: python

    import storm_scheduler

    schedule = storm_scheduler.Scheduler()
    schedule.task(hello_world).every(3)
    schedule.task(my_function).every(5, 'minutes')
    schedule.loop()
