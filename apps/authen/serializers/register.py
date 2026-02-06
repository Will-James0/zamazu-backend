from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password", "phone", "is_active")
        extra_kwargs = {
            "is_active": {"allow_null": True},
        }