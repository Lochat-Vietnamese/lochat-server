# import uuid
# from django.db import models
# from django.utils.timezone import now
# from app.entities.accountsConversations import AccountsConversations
# from app.entities.conversations import Conversations
# from app.enums.messageTypes import MessageTypes
# from app.entities.medias import Medias

# class Messages(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE, related_name="ConversationRelated")
#     sender_relation = models.ForeignKey(AccountsConversations, on_delete=models.CASCADE, related_name='MessagesSent')
#     type = models.CharField(max_length=50, choices=MessageTypes.choices, default=MessageTypes.TEXT)
#     content = models.TextField(null = True)
#     media = models.ForeignKey(Medias, null=True ,on_delete=models.SET_NULL)
#     reply_to = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=now)
#     updated_at = models.DateTimeField(null=True)

#     @property
#     def get_sender(self):
#         return self.sender_relation.account
    
#     class Meta:
#         app_label = "app"

#     class Meta:
#         indexes = [
#             models.Index(fields=['conversation', 'created_at']),
#         ]