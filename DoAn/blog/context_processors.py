from .models import Blog


def latest_blog(request):
    return {
        "latest_blog_post": Blog.objects.order_by('-created_at', '-id').first(),
    }
