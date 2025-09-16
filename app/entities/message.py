import uuid
from django.db import models
from django.utils.timezone import now
from app.entities.profileConversation import ProfileConversation
from app.entities.conversation import Conversation
from app.enums.messageTypes import MessageTypes
from app.entities.media import Media

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="message_conversation")
    sender = models.ForeignKey(ProfileConversation, on_delete=models.CASCADE, related_name='message_sender')
    type = models.CharField(max_length=10, choices=MessageTypes.choices, default=MessageTypes.TEXT)
    content = models.TextField(null = True)
    media = models.ForeignKey(Media, null=True ,on_delete=models.SET_NULL, related_name="message_media")
    reply = models.UUIDField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)
    
    class Meta:
        app_label = "app"
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]