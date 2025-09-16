from rest_framework import serializers
from app.entities.profile import Profile


class ProfileMapping(serializers.ModelSerializer):
    hometown = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "nickname",
            "phone_number",
            "dob",
            "bio",
            "avatar_url",
            "address",
            "hometown",
            "education",
            "work",
            "hobbies"
        ]
        read_only_fields = ["id"]

    def get_hometown(self, obj):
        if obj.hometown:
            return obj.get_hometown_display()
        return None
