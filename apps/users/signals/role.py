from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.users.models import Role
from apps.users.enums import RoleEnum

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    for role in RoleEnum:
        Role.objects.get_or_create(code=role.value, defaults={'name': role.label})