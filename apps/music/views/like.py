from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.music.models import Like, Track, Clip, Album
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType


class ToggleLikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, content_type, code):
        models_map = {
            'track': Track,
            'clip': Clip,
            'album': Album,
        }
        
        model = models_map.get(content_type)
        if not model:
            return Response({"error": "Invalid content type."}, status=400)
        
        try:
            obj = model.objects.get(code=code)
        except model.DoesNotExist:
            return Response({"error": f"{content_type} not found."}, status=404)
        
        content_type_obj = ContentType.objects.get_for_model(model)
        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type=content_type_obj,
            object_id=obj.id
        )
        
        if not created:
            like.delete()
            return Response({
                "liked": False,
                "likes_count": obj.likes.count()
            }, status=200)

        return Response({
            "liked": True,
            "likes_count": obj.likes.count()
        }, status=201)