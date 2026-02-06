from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .role import Role


class User(AbstractUser):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='user_profiles', null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    
    
    def __str__(self):
        return self.username