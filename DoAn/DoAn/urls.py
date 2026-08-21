from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.shortcuts import render
from users.views import register_view, login_view, custom_logout
from blog.views import blog_list, blog_detail, rate_blog

def index(request):
    return render(request, 'index.html')

def shop(request):
    return render(request, 'shop.html')


def product_details(request):
    return render(request, 'product-details.html')

urlpatterns = [
    path('', index, name='index'),
    path('shop/', shop, name='shop'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('product-details/', product_details, name='product_details'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/<int:pk>/', blog_detail, name='blog_detail'),
    path('blog/<int:pk>/rate/', rate_blog, name='rate_blog'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('users/logout/', custom_logout, name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
