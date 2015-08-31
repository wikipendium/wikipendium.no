from wikipendium.jitishcron import registered_tasks
from wikipendium.jitishcron.models import TaskExecution
from datetime import timedelta
from django.utils import timezone
from django.db import IntegrityError
import functools


def task(fn=None, key=None, min_interval_in_seconds=0):

    if fn is None:
        return functools.partial(
            task, key=key, min_interval_in_seconds=min_interval_in_seconds)

    if key is None:
        key = '%s.%s' % (fn.__module__, fn.__name__)

    def inner(*args, **kwargs):
        time_limit = timezone.now() - timedelta(
            seconds=min_interval_in_seconds)
        previous_task_execution = TaskExecution.objects.filter(
            key=key).order_by('-time').first()
        should_execute_task = (previous_task_execution is None or
                               previous_task_execution.time < time_limit)
        if should_execute_task:
            execution_number = (previous_task_execution.execution_number + 1
                                if previous_task_execution is not None
                                else 0)
            try:
                TaskExecution.objects.create(
                    key=key, execution_number=execution_number)
                return fn(*args, **kwargs)
            except IntegrityError:
                pass

    registered_tasks.append(inner)

    return inner
