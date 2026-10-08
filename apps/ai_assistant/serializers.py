from rest_framework import serializers
from .models import AIConversation, AIMessage, AIObservabilityLog

class AIMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIMessage
        fields = '__all__'

class AIConversationSerializer(serializers.ModelSerializer):
    messages = AIMessageSerializer(many=True, read_only=True)

    class Meta:
        model = AIConversation
        fields = '__all__'

class AIObservabilityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIObservabilityLog
        fields = '__all__'
