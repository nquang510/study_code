from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Blog


def blog_list(request):
    blogs = Blog.objects.select_related('author').order_by('-created_at', '-id')

    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {
        'page_obj': page_obj,
    })


def blog_detail(request, pk):
    blog = get_object_or_404(Blog.objects.select_related('author'), pk=pk)

    next_post = (
        Blog.objects.filter(
            Q(created_at__lt=blog.created_at)
            | Q(created_at=blog.created_at, id__lt=blog.id)
        )
        .order_by('-created_at', '-id')
        .first()
    )
    
    prev_post = (
        Blog.objects.filter(
            Q(created_at__gt=blog.created_at)
            | Q(created_at=blog.created_at, id__gt=blog.id)
        )
        .order_by('created_at', 'id')
        .first()
    )

    return render(request, 'blog-detail.html', {
        'blog': blog,
        'next_post': next_post,
        'prev_post': prev_post,
    })
