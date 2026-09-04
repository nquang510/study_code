from django.urls import path
from . import views

# Tat ca route trong file nay deu nam duoi prefix "account/"
# -> /account/update/, /account/my-product/, /account/add-product/
urlpatterns = [
    path("update/", views.account_update, name="account_update"),
    path("my-product/", views.my_product, name="my_product"),
    path("add-product/", views.add_product, name="add_product"),
]
