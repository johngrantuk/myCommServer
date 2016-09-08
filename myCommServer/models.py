from django.db import models
from django.utils import timezone


class MyCommDevice(models.Model):
    """
    Model for a MyComm device.
    """
    imei = models.TextField(primary_key=True)                               # IMEI of Iridium.
    deviceId = models.TextField(unique=True)                                # Unique ID of MyComm device.
    createdDate = models.DateTimeField(default=timezone.now)                # Time stamp when created.


class MyCommMsg(models.Model):
    """
    Model for a message sent from a MyComm device.
    """
    deviceImei = models.ForeignKey(MyCommDevice, on_delete=models.CASCADE)  # ID of MyComm that message has come from.
    message = models.TextField()                                            # Main message text.
    destinationId = models.TextField()                                      # Onward message info.
    receivedTime = models.DateTimeField(default=timezone.now)               # Time stamp of time received on server.
    longitude = models.TextField()                                          # Device lng (from message info)
    latitude = models.TextField()                                           # Device lat (from message info)
    iridium_cep=  models.TextField()                                        # Position accuracy (from message info)
    transmit_time = models.TextField()                                      # Message transmit time (from message info)


class UserMsg(models.Model):
    """
    Model for a message sent to a MyComm device from a user using something like web interface, etc.
"""
    user = models.ForeignKey('auth.User')                                   # User will have to be registered and logged in.
    message = models.TextField()                                            # Main message text.
    destinationId = models.TextField()                                      # ID of MyComm device to send to - i.e. myCommHackaday.
    receivedTime = models.DateTimeField(default=timezone.now)               # Time stamp.

    def receive(self):
        self.receivedDate = timezone.now()
        self.save()

    def getMessage(self):
        return self.message
