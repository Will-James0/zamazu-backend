from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.users.models import User

class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        if email and password:

            user = authenticate(email=email, password=password)
            
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        
        self.user = user
        
        refresh = self.get_token(user)
        
        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        data["user"] = {
            "code": str(user.code),
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "image": user.image.url if user.image else None,
            "phone": user.phone,
            "role": {
                "code": user.role.code if user.role else None,
                "name": user.role.name if user.role else None,
            }
        }
        
        
        data["access_expires_in"] = api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()
        data["refresh_expires_in"] = api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()
        
        return data