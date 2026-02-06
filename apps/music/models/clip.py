from django.db import models
import uuid
from .track import Track
from django.contrib.contenttypes.fields import GenericRelation

class Clip(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='clips')
    video_file = models.FileField(upload_to='clips/video_files/')
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation('Like')
    comments = GenericRelation('Comment')
    views = GenericRelation('View')

    def __str__(self):
        return self.track.title + " Clip"