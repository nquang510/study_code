from django.db import models
from django.utils import timezone
from django.conf import settings

class Demo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    img = models.ImageField(upload_to='demo_images/', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'demo'