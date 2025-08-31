import uuid
from django.db import models
from app.enums.provinces import Provinces

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    dob = models.DateField()
    bio = models.TextField(null=True)
    avatar_url = models.TextField(null=True)
    address = models.TextField(null=True)
    hometown = models.CharField(max_length=50, choices=Provinces.choices, null=True)
    education = models.CharField(max_length=255, null=True)
    work = models.CharField(max_length=255, null=True)
    hobbies = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "app"
        indexes = [
            models.Index(fields=['nickname']),
        ]