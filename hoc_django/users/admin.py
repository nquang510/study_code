from django.contrib import admin
from .models import CustomerUser, Country

admin.site.register(CustomerUser)
admin.site.register(Country)