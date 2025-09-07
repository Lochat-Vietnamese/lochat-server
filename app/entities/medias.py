# import uuid
# from django.db import models
# from django.utils.timezone import now
# from app.entities.accountsConversations import AccountsConversations
# from app.enums.mediaTypes import MediaTypes

# class Medias(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     uploader = models.ForeignKey(AccountsConversations, on_delete=models.SET_NULL, null=True, related_name='UploadedMedias')
#     name = models.CharField(max_length=255)
#     type = models.CharField(max_length=50, choices=MediaTypes.choices, default=MediaTypes.UNKNOW)
#     size = models.BigIntegerField()
#     url = models.TextField()
#     duration = models.FloatField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=now)
#     updated_at = models.DateTimeField(null=True, blank=True)

#     @property
#     def get_uploader(self):
#         return self.uploader_relation.account

#     @property
#     def get_conversation(self):
#         return self.uploader_relation.conversation

#     class Meta:
#         app_label = "app"