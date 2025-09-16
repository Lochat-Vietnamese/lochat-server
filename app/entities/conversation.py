import uuid
from django.db import models
from django.utils.timezone import now
from app.entities.profile import Profile
from app.enums.conversationTypes import ConversationTypes

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=True)
    avatar_url = models.TextField(null=True)
    type = models.CharField(max_length=20, choices=ConversationTypes.choices, default=ConversationTypes.PRIVATE)
    creator = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='conversation_creator')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = "app"