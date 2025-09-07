# import uuid
# from django.db import models
# from django.utils.timezone import now
# from app.entities.account import Accounts

# class Conversations(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255, null=True, blank=True)
#     avatar_url = models.TextField(null=True, blank=True)
#     is_group = models.BooleanField(default=False)
#     is_community = models.BooleanField(default=False)
#     creator = models.ForeignKey(Accounts, on_delete=models.SET_NULL, null=True, related_name='CreatedConversations')
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=now)
#     updated_at = models.DateTimeField(null=True, blank=True)
    
#     class Meta:
#         app_label = "app"