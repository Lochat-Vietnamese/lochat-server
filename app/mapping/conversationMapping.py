from rest_framework import serializers
from app.entities.conversation import Conversation
from app.mapping.profileMapping import ProfileMapping

class ConversationMapping(serializers.ModelSerializer):
    creator = ProfileMapping(read_only=True)
    class Meta:
        model = Conversation
        fields = [
            "id",
            "title",
            "avatar_url",
            "type",
            "creator"
        ]
        read_only_fields = ["id"]
