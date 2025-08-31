from django.db import models

class RelationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"