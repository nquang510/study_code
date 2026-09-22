from django.contrib import admin
from .models import Country, User, Category, Brand, Product, History


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Country, CountryAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id_country')
admin.site.register(User, UserAdmin)

admin.site.register(Category)
admin.site.register(Brand)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'id_user', 'price', 'created_at')
admin.site.register(History, HistoryAdmin)
