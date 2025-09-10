from rest_framework import serializers
from app.entities.message import Message
from app.mapping.conversationMapping import ConversationMapping
from app.mapping.profileConversationMapping import ProfileConversationMapping

class MessageMapping(serializers.ModelSerializer):
    conversation = ConversationMapping(read_only=True)
    sender = ProfileConversationMapping(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "sender",
            "type",
            "content",
            "media",
            "reply"
        ]
        read_only_fields = ['id']
