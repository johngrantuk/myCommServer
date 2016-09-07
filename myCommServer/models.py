from django.db import models
from django.utils import timezone


class UserMsg(models.Model):
    user = models.ForeignKey('auth.User')
    message = models.TextField()
    destinationId = models.TextField()
    receivedDate = models.DateTimeField(default=timezone.now)

    def receive(self):
        self.receivedDate = timezone.now()
        self.save()

    def getMessage(self):
        return self.message
