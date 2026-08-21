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
