from django.urls import path
from . import views

urlpatterns = [
    path("update/", views.account_update, name="account_update"),
    path("my-product/", views.my_product, name="my_product"),
    path("add-product/", views.add_product, name="add_product"),
    path("add-product/ajax/", views.add_product_ajax, name="add_product_ajax"),
    path("edit-product/<int:pk>/", views.edit_product, name="edit_product"),
    path("edit-product/<int:pk>/ajax/", views.edit_product_ajax, name="edit_product_ajax"),
    path("delete-product/<int:pk>/", views.delete_product, name="delete_product"),
    path('product-details/<int:pk>/', views.product_details, name='product_details'),
]
