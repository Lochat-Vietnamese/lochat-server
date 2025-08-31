from rest_framework import serializers
from app.entities.relation import Relation
from app.mapping.profileMapping import ProfileMapping


class RelationMapping(serializers.ModelSerializer):
    requester = ProfileMapping(read_only=True)
    receiver = ProfileMapping(read_only=True)

    class Meta:
        model = Relation
        fields = [
            "id",
            "type",
            "requester",
            "receiver",
            "status"
        ]
        read_only_fields = ["id"]
