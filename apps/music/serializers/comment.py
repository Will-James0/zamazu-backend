from rest_framework import serializers
from apps.music.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_code = serializers.CharField(source='user.code', read_only=True)
    user_image = serializers.ImageField(source='user.image', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_code', 'user_image', 'text', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']