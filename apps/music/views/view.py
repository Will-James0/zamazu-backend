from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.music.models import View, Track, Clip, Album
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType


class RecordViewView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, content_type, code):
        models_map = {
            'track': Track,
            'clip': Clip,
        }
        
        model = models_map.get(content_type)
        if not model:
            return Response({"error": "Invalid content type."}, status=400)
        
        try:
            obj = model.objects.get(code=code)
        except model.DoesNotExist:
            return Response({"error": f"{content_type} not found."}, status=404)
        
        content_type_obj = ContentType.objects.get_for_model(model)
        view, created = View.objects.get_or_create(
            user=request.user,
            content_type=content_type_obj,
            object_id=obj.id
        )
        
        return Response({
            "viewed": True,
            "views_count": obj.views.count(),
            "first_view": created
        }, status=200)