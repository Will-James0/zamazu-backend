from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation

class Track(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    album = models.ForeignKey('Album', on_delete=models.SET_NULL, null=True, related_name='tracks')
    cover_image = models.ImageField(upload_to='tracks/covers/', null=True, blank=True)
    audio_file = models.FileField(upload_to='tracks/audio_files/')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    likes = GenericRelation('Like')
    comments = GenericRelation('Comment')
    views = GenericRelation('View')
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title