from rest_framework import serializers
from app.entities.media import Media
from app.mapping.profileConversationMapping import ProfileConversationMapping


class MediasMapping(serializers.ModelSerializer):
    uploader = ProfileConversationMapping(read_only=True)

    class Meta:
        model = Media
        fields = [
            "id",
            "uploader",
            "name",
            "type",
            "size",
            "url"
        ]
        read_only_fields = ["id"]
