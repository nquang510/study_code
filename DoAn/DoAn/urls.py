from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.shortcuts import render, get_object_or_404
from users.views import register_view, login_view, custom_logout
from blog.views import blog_list, blog_detail, rate_blog, comment_blog
from users.models import Product

def index(request):
    products = Product.objects.order_by('-created_at', '-id')[:6]
    return render(request, 'index.html', {'products': products})

def shop(request):
    return render(request, 'shop.html')


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # tinh gia sau khi giam de khoi phai tinh trong template
    gia_sale = None
    if product.status == 1 and product.sale:
        gia_sale = product.price * (100 - product.sale) / 100

    return render(request, 'product_details.html', {
        'product': product,
        'gia_sale': gia_sale,
    })

urlpatterns = [
    path('', index, name='index'),
    path('shop/', shop, name='shop'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('product-details/<int:pk>/', product_details, name='product_details'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/<int:pk>/', blog_detail, name='blog_detail'),
    path('blog/<int:pk>/rate/', rate_blog, name='rate_blog'),
    path('blog/<int:pk>/comment/', comment_blog, name='comment_blog'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('users/logout/', custom_logout, name='logout'),
    path('account/', include('users.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
