from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.authen.serializers.register import RegisterUserSerializer
from core.utils import *
from apps.users.models import Role
from apps.users.enums import RoleEnum

logger = logging.getLogger(__name__)

User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    
    def perform_create(self, serializer):
        mdp = serializer.validated_data.get('password')
        role = Role.objects.get(code=RoleEnum.MEMBER.value)
        serializer.save(password=make_password(mdp), role=role)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # user = serializer.instance
        # subject = "✅ Votre demande d'inscription a été acceptée !"
        # message = format_registration_accepted()
        # send_user_email(
        #     subject=subject,
        #     message=message,
        #     recipient_list=[user.email]
        # )
        return Response({
            "message": "Compte créé avec succès ! Un message d'activation a été envoyé à votre adresse e-mail."
        }, status=status.HTTP_201_CREATED)