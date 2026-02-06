from rest_framework import serializers
from apps.music.models import Album, Track, Like
from django.contrib.contenttypes.models import ContentType

class AbumPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['code', 'title', 'cover_image', 'slug', 'release_date']
        extra_kwargs = {
            'code': {'read_only': True}, 'title': {'read_only': True},
            'cover_image': {'read_only': True}, 'slug': {'read_only': True},
            'release_date': {'read_only': True},
        }
        
class TrackSerializer(serializers.ModelSerializer):
    album = AbumPublicSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'code', 'title', 'album', 'cover_image', 'audio_file', 'slug',
            'release_date', 'created_at', 'updated_at',
            'likes_count', 'is_liked', 'views_count'
        ]
        extra_kwargs = {
            'code': {'read_only': True}, 'title': {'read_only': True},
            'album': {'read_only': True}, 'cover_image': {'read_only': True},
            'audio_file': {'read_only': True}, 'slug': {'read_only': True},
            'release_date': {'read_only': True},
            'created_at': {'read_only': True}, 'updated_at': {'read_only': True},
        }
        
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(Track)
            return Like.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False
    
    def get_views_count(self, obj):
        return obj.views.count()
        

class CreateTrackSerializer(serializers.ModelSerializer):
    album = AbumPublicSerializer(read_only=True)
    
    class Meta:
        model = Track
        fields = [
            'title', 'album', 'cover_image', 'audio_file', 'release_date'
        ]
        extra_kwargs = {
            'album': {'allow_null': True}, 'cover_image': {'allow_null': True},
            'release_date': {'allow_null': True},
        }
        
class UpdateTrackSerializer(serializers.ModelSerializer):
    album = AbumPublicSerializer(read_only=True)
    
    class Meta:
        model = Track
        fields = [
            'title', 'album', 'cover_image', 'audio_file', 'release_date'
        ]
        extra_kwargs = {
            'title': {'allow_null': True},
            'album': {'allow_null': True},
            'cover_image': {'allow_null': True},
            'audio_file': {'allow_null': True, 'required': False},
            'release_date': {'allow_null': True},
        }
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        
        # Gérer la mise à jour de l'album
        album_data = validated_data.get('album')
        if album_data:
            album_serializer = AbumPublicSerializer(instance.album, data=album_data, partial=True)
            if album_serializer.is_valid():
                album_serializer.save()
        
        # Gérer la mise à jour de la cover_image
        cover_image = validated_data.get('cover_image')
        if cover_image is not None:
            if instance.cover_image:
                instance.cover_image.delete(save=False)
            instance.cover_image = cover_image
        
        # Gérer la mise à jour du audio_file
        audio_file = validated_data.get('audio_file')
        if audio_file is not None:
            if instance.audio_file:
                instance.audio_file.delete(save=False)
            instance.audio_file = audio_file
        
        instance.save()
        return instance