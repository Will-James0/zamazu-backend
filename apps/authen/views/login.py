from rest_framework_simplejwt.views import TokenObtainPairView
from apps.authen.serializers import AuthTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status

class LoginAPIView(TokenObtainPairView):
    """
    Vue API pour l'authentification par token
    Permet de se connecter avec l'email
    """
    serializer_class = AuthTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    

class AdminLoginAPIView(TokenObtainPairView):
    """
    Vue API pour l'authentification par token des administrateurs
    Permet de se connecter avec l'email
    """
    serializer_class = AuthTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.user
        if not user.role.code in ['owner', 'administrator', 'moderator']:
            return Response(
                {"detail": "Accès refusé. Seuls les administrateurs peuvent se connecter ici."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(serializer.validated_data)