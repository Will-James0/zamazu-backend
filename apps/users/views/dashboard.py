from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsStaffMember
from apps.music.models import Track, Clip, Like, Comment, View

User = get_user_model()

class DashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStaffMember]

    def get(self, request):
        data = {
            "counts": {
                "users": User.objects.count(),
                "tracks": Track.objects.count(),
                "clips": Clip.objects.count(),
                "likes": Like.objects.count(),
                "comments": Comment.objects.count(),
                "views": View.objects.count(),
            },
            "latest": {
                "users": list(
                    User.objects.order_by('-date_joined')[:3]
                    .values("code", "username", "email", "date_joined")
                ),
                "tracks": list(
                    Track.objects.order_by('-created_at')[:3]
                    .values("code", "title", "created_at")
                )
            }
        }

        return Response(data, status=status.HTTP_200_OK)
