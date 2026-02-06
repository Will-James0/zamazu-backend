from rest_framework import serializers
from apps.music.models import Clip, Track, Like
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

class TrackPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['code', 'title', 'cover_image', 'slug', 'release_date']
        extra_kwargs = {
            'code': {'read_only': True}, 'title': {'read_only': True},
            'cover_image': {'read_only': True}, 'slug': {'read_only': True},
            'release_date': {'read_only': True},
        }
        
class ClipSerializer(serializers.ModelSerializer):
    track = TrackPublicSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Clip
        fields = [
            'code', 'track', 'video_file', 'release_date',
            'created_at', 'updated_at', 
            'likes_count', 'is_liked', 'views_count'
        ]
        extra_kwargs = {
            'code': {'read_only': True}, 'track': {'read_only': True},
            'video_file': {'read_only': True}, 'release_date': {'read_only': True},
            'created_at': {'read_only': True}, 'updated_at': {'read_only': True},
        }
        
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(Clip)
            return Like.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False
    
    def get_views_count(self, obj):
        return obj.views.count()
        

class CreateClipSerializer(serializers.ModelSerializer):
    track = TrackPublicSerializer(read_only=True)
    track_code = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Clip
        fields = [
            'track', 'video_file', 'release_date', 'track_code'
        ]
        extra_kwargs = {
            'release_date': {'allow_null': True},
        }
        
    def create(self, validated_data):
        track_code = validated_data.pop('track_code')
        track = get_object_or_404(Track, code=track_code)
        clip = Clip.objects.create(track=track, **validated_data)
        return clip
        

class UpdateClipSerializer(serializers.ModelSerializer):
    track = TrackPublicSerializer(read_only=True)
    track_code = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Clip
        fields = [
            'track', 'video_file', 'release_date', 'track_code'
        ]
        extra_kwargs = {
            'track': {'allow_null': True},
            'video_file': {'allow_null': True, 'required': False},
            'release_date': {'allow_null': True},
            'track_code': {'allow_null': True},
        }
        
    def update(self, instance, validated_data):
        track = validated_data.get('track', None)
        video_file = validated_data.get('video_file', None)
        release_date = validated_data.get('release_date', None)
        track_code = validated_data.get('track_code', None)
        
        
        if track_code is not None:
            track = get_object_or_404(Track, code=track_code)
            instance.track = track
        
        if video_file is not None:
            if instance.video_file:
                instance.video_file.delete(save=False)
            instance.video_file = video_file
        
        if release_date is not None:
            instance.release_date = release_date
        
        instance.save()
        return instance