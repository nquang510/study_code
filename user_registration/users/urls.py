from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_users, name='list_users'),
    path('add/', views.add_user, name='add_user'),
    path('edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
]