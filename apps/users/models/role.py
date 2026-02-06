from django.db import models
from apps.users.enums import RoleEnum

class Role(models.Model):
    code = models.CharField(max_length=20, choices=RoleEnum.choices, unique=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name