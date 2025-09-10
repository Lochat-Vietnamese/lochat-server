import uuid
from django.db import models
from django.utils.timezone import now
from app.entities.profileConversation import ProfileConversation
from app.enums.mediaTypes import MediaTypes

class Media(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploader = models.ForeignKey(ProfileConversation, on_delete=models.CASCADE, null=True, related_name='media_uploader')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=MediaTypes.choices, default=MediaTypes.UNKNOW)
    size = models.BigIntegerField()
    url = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "app"
        unique_together = ('uploader', 'url')
        indexes = [
            models.Index(fields=['uploader']),
        ]