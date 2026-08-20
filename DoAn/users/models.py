from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    User tuỳ biến kế thừa AbstractUser của Django.

    AbstractUser đã cung cấp sẵn: username, password (đã hash),
    email, first_name, last_name, is_staff, is_active, is_superuser,
    last_login, date_joined, groups, user_permissions cùng toàn bộ
    cơ chế xác thực/permission chuẩn của Django (set_password,
    check_password, authenticate, login_required, admin site, ...).
    Ở đây ta chỉ cần bổ sung các field riêng của dự án.
    """

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    id_country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Country",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
