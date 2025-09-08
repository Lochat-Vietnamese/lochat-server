from django.db import models

class ConversationTypes(models.TextChoices):
    PRIVATE = "private", "Private"
    GROUP = "group", "Group"
    COMMUNITY = "community", "Community"
