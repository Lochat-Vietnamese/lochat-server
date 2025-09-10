import uuid
from django.db import models
from django.utils.timezone import now
from app.entities.profile import Profile
from app.entities.conversation import Conversation

class ProfileConversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profileConversation_profile')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='profileConversation_conversation')
    last_accessed = models.DateTimeField(default=now)
    conversation_name = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        app_label = "app"
        unique_together = ('profile', 'conversation')
        indexes = [
            models.Index(fields=['last_accessed']),
        ]