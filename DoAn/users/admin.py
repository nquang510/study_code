from django.contrib import admin
from .models import Country, User


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "id_country")
    list_filter = ("id_country",)
    search_fields = ("username", "email")
    autocomplete_fields = ("id_country",)