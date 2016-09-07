from .models import UserMsg
from rest_framework import serializers


class UserMsgSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserMsg
        fields = ('user', 'message', 'destinationId', 'receivedDate')
