import uuid
from django.db import models
from app.entities.profile import Profile
from app.enums.relationStatus import RelationStatus
from app.enums.relationTypes import RelationTypes

class Relation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=RelationTypes.choices, default=RelationTypes.FRIEND)
    first_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="relation_first_user")
    second_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="relation_second_user")
    status = models.CharField(max_length=20, choices=RelationStatus.choices, default=RelationStatus.PENDING)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "app"
        indexes = [
            models.Index(fields=["first_user", "second_user"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["first_user", "second_user"],
                name="unique_relation_pair"
            )
        ]

    def save(self, *args, **kwargs):
        if self.first_user.id > self.second_user.id:
            self.first_user, self.second_user = self.second_user, self.first_user
        super().save(*args, **kwargs)