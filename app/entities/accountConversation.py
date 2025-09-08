import uuid
from django.db import models
from django.utils.timezone import now
from app.entities.account import Account
from app.entities.conversation import Conversation

class AccountConversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accountConversation_account')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='accountConversation_conversation')
    last_accessed = models.DateTimeField(default=now)
    conversation_name = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        app_label = "app"
        unique_together = ('account', 'conversation')
        indexes = [
            models.Index(fields=['last_accessed']),
        ]