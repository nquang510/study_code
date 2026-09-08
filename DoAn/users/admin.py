from django.contrib import admin
from .models import Country, User, Category, Brand, Product


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Country, CountryAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id_country')
admin.site.register(User, UserAdmin)

admin.site.register(Category)
admin.site.register(Brand)