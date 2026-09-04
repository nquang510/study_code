from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Blog, Comment, Rate


def blog_list(request):
    blogs = Blog.objects.select_related('author').order_by('-created_at', '-id')

    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog-list.html', {
        'page_obj': page_obj,
    })


def blog_detail(request, pk):
    blog = get_object_or_404(Blog.objects.select_related('author'), pk=pk)
    average_rating = round(Rate.objects.filter(id_blog=blog).aggregate(Avg('rate'))['rate__avg'] or 0)
    rate_count = Rate.objects.filter(id_blog=blog).count()
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
    check = False
    if request.user.is_authenticated:
        check = Rate.objects.filter(id_blog=blog, id_user=request.user).exists()

    # chi lay comment cha, comment con lay qua cmt.replies.all trong template
    comments = (
        Comment.objects.filter(id_blog=blog, parent__isnull=True)
        .select_related('id_user')
        .prefetch_related('replies__id_user')
    )
    comment_count = Comment.objects.filter(id_blog=blog).count()

    return render(request, 'blog-detail.html', {
        'blog': blog,
        'next_post': next_post,
        'prev_post': prev_post,
        'average_rating': average_rating,
        'rate_count': rate_count,
        'check': check,
        'stars': range(1, 6),
        'comments': comments,
        'comment_count': comment_count,
    })


@require_POST
def rate_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'Vui lòng đăng nhập để đánh giá bài viết.',
        })

    try:
        rate_value = int(request.POST.get('rate'))
    except (TypeError, ValueError):
        return JsonResponse({
            'success': False,
            'message': 'Điểm đánh giá không hợp lệ.',
        })

    if rate_value < 1 or rate_value > 5:
        return JsonResponse({
            'success': False,
            'message': 'Điểm đánh giá phải từ 1 đến 5.',
        })

    if Rate.objects.filter(id_blog=blog, id_user=request.user).exists():
        return JsonResponse({
            'success': False,
            'message': 'Bạn đã đánh giá bài viết này rồi.',
        })

    Rate.objects.create(id_blog=blog, id_user=request.user, rate=rate_value)

    average_rating = round(Rate.objects.filter(id_blog=blog).aggregate(Avg('rate'))['rate__avg'] or 0)
    rate_count = Rate.objects.filter(id_blog=blog).count()

    return JsonResponse({
        'success': True,
        'message': 'Cảm ơn bạn đã đánh giá!',
        'average_rating': average_rating,
        'rate_count': rate_count,
    })


@require_POST
def comment_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if not request.user.is_authenticated:
        messages.error(request, 'Vui lòng đăng nhập để bình luận.')
        return redirect('login')

    content = (request.POST.get('content') or '').strip()
    if not content:
        messages.error(request, 'Nội dung bình luận không được để trống.')
        return redirect('blog_detail', pk=blog.pk)

    parent = None
    parent_id = request.POST.get('parent_id')
    if parent_id and parent_id.isdigit():
        parent = Comment.objects.filter(pk=parent_id, id_blog=blog).first()
        if parent and parent.parent_id:
            parent = parent.parent

    Comment.objects.create(
        id_blog=blog,
        id_user=request.user,
        content=content,
        parent=parent,
    )

    messages.success(request, 'Đã gửi bình luận.')
    return redirect('blog_detail', pk=blog.pk)
