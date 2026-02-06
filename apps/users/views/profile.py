from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers import ProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsProfileOwner

User = get_user_model()



class ProfileMixinView(generics.GenericAPIView,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin):
    
    queryset = User.objects.all()
    lookup_field = 'code'
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsProfileOwner]
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('code')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)