"""
URL configuration for DoAn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.shortcuts import render
from users.views import register_view, login_view, custom_logout

def index(request):
    return render(request, 'index.html')

def shop(request):
    return render(request, 'shop.html')


def product_details(request):
    return render(request, 'product-details.html')

def blog_detail(request):
    return render(request, 'blog-detail.html')
def blog_list(request):
    return render(request, 'blog.html')

urlpatterns = [
    path('', index, name='index'),
    path('shop/', shop, name='shop'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('product-details/', product_details, name='product_details'),
    path('blog-detail/', blog_detail, name='blog_detail'),
    path('blog/', blog_list, name='blog_list'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('users/logout/', custom_logout, name='logout'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)