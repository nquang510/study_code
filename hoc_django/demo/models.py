from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

class Demo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    img = models.ImageField(upload_to='demo_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'demo'

image = models.ImageField(upload_to='demo_images/', null=True, blank=True)
        