from rest_framework import serializers
from apps.music.models import Album

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = [
            'code', 'title', 'cover_image', 'slug', 'created_at', 'updated_at', 'release_date'
        ]
        read_only_fields = ['code', 'slug', 'created_at', 'updated_at']
        

class CreateAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = [
            'title', 'cover_image', 'release_date'
        ]
        extra_kwargs = {
            'release_date': {'allow_null': True},
        }
        
        
class UpdateAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = [
            'title', 'cover_image', 'release_date'
        ]
        extra_kwargs = {
            'title': {'allow_null': True},
            'cover_image': {'allow_null': True},
            'release_date': {'allow_null': True},
        }
        
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        cover_image = validated_data.get('cover_image', None)
        
        if cover_image is not None:
            if instance.cover_image:
                instance.cover_image.delete(save=False)
            instance.cover_image = cover_image