from rest_framework import serializers

from .models import ChatMessage
from .models import Temperature


class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = ['id', 'type', 'temperature', 'humidity', 'pressure', 'date']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
