from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation

class Album(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='albums/covers/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation('Like')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title