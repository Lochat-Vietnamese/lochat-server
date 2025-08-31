import uuid
from django.db import models
from django.utils.timezone import now
from app.entities.account import Accounts
from app.entities.conversations import Conversations

class AccountsConversations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='RelatedAccountsConversations')
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE, related_name='RelatedAccountsConversations')
    last_accessed = models.DateTimeField(default=now)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(null=True)

    @property
    def get_account(self):
        return self.account

    @property
    def get_conversation(self):
        return self.conversation

    class Meta:
        app_label = "app"
        unique_together = ('account', 'conversation')

    class Meta:
        indexes = [
            models.Index(fields=['account', 'last_accessed']),
        ]