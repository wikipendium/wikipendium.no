from django.db import models
from django.utils import timezone


class TaskExecution(models.Model):
    time = models.DateTimeField(default=timezone.now)
    key = models.CharField(max_length=256)
    execution_number = models.IntegerField()

    class Meta:
        unique_together = ('key', 'execution_number')
        app_label = 'jitishcron'

    def __unicode__(self):
        return '%s:%s' % (self.key, self.time)
