from rest_framework import serializers
from app.entities.account import Account
from app.mapping.profileMapping import ProfileMapping


class AccountMapping(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileMapping(read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "profile",
            "username",
            "email",
            "password"
        ]
        read_only_fields = ["id"]
