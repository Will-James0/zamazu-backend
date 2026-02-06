from django.db import models

class RoleEnum(models.TextChoices):
    OWNER = 'owner', 'Propriétaire'
    ADMINISTRATOR = 'administrator', 'Administrateur'
    MODERATOR = 'moderator', 'Modérateur'
    MEMBER = 'member', 'Membre'