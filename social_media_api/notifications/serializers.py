from rest_framework import serializers
from .models import Notification

class NotificationsSerialize(serializers.ModelSerialize):
    actor_name = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'actor_name', 'verb', 'timestamp', 'is_read']

