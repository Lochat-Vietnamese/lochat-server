import uuid
from django.db import models
from app.entities.profile import Profile
from app.enums.relationStatus import RelationStatus
from app.enums.relationTypes import RelationTypes

class Relation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=RelationTypes.choices, default=RelationTypes.FRIEND)
    requester = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="relation_requester")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="relation_receiver")
    status = models.CharField(max_length=20, choices=RelationStatus.choices, default=RelationStatus.PENDING)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "app"
        indexes = [
            models.Index(fields=["requester", "receiver"]),
        ]
        unique_together = ("requester", "receiver")
