from rest_framework import serializers
from app.entities.profileConversation import ProfileConversation
from app.mapping.conversationMapping import ConversationMapping
from app.mapping.profileMapping import ProfileMapping

class ProfileConversationMapping(serializers.ModelSerializer):
    profile = ProfileMapping(read_only=True)
    conversation = ConversationMapping(read_only=True)
    class Meta:
        model = ProfileConversation
        fields = [
            "id",
            "profile",
            "conversation",
            "last_accessed",
            "conversation_name"
        ]
        read_only_fields = ['id']
