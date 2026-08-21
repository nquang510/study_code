from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField


class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, help_text="Mô tả ngắn / tóm tắt bài viết")
    content = RichTextUploadingField()
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs",
    )

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
class Rate(models.Model):
    id_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="rates")
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rates")
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ("id_blog", "id_user")
    def __str__(self):
        return f"{self.id_user.username} - {self.id_blog.title} - {self.rate}"