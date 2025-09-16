from django.db import models

class RelationTypes(models.TextChoices):
    FRIEND = "FRIEND", "Friend"
    FOLLOW = "FOLLOW", "Follow"
    BLOCK = "BLOCK", "Block"