import os

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Country, User, Category, Brand, Product, History

# an link "View site" tren trang admin (admin khong duoc vao frontend)
admin.site.site_url = None


def xoa_hinh_san_pham(product):
    # xoa file anh trong media/products khi xoa san pham
    save_folder = os.path.join(settings.MEDIA_ROOT, "products")
    for img in product.images or []:
        path = os.path.join(save_folder, img)
        if os.path.exists(path):
            os.remove(path)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Country, CountryAdmin)


# ===== List user =====
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'id_country', 'level', 'is_active')
    list_display_links = ('id', 'username')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'id_country')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('-id',)

    # them cac field rieng cua User vao form edit / add
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Thông tin thêm', {'fields': ('avatar', 'phone', 'id_country')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Thông tin thêm', {'fields': ('email', 'first_name', 'last_name', 'avatar', 'phone', 'id_country')}),
    )

    @admin.display(description='Level')
    def level(self, obj):
        if obj.is_superuser or obj.is_staff:
            return format_html('<b style="color:#d9534f;">{}</b>', 'Admin')
        return format_html('<span style="color:#5cb85c;">{}</span>', 'Member')

    # xoa user thi product cua user cung bi xoa (CASCADE) -> xoa luon file anh
    def delete_model(self, request, obj):
        for product in obj.products.all():
            xoa_hinh_san_pham(product)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for product in Product.objects.filter(id_user__in=queryset):
            xoa_hinh_san_pham(product)
        super().delete_queryset(request, queryset)
admin.site.register(User, UserAdmin)

admin.site.register(Category)
admin.site.register(Brand)


# ===== List product =====
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'hinh', 'name', 'member', 'price', 'id_category', 'id_brand', 'trang_thai', 'created_at')
    list_display_links = ('id', 'name')
    list_filter = ('status', 'id_category', 'id_brand')
    # tim kiem product theo ten member (username / ho / ten)
    search_fields = ('id_user__username', 'id_user__first_name', 'id_user__last_name')
    search_help_text = 'Tìm theo tên member (username, họ, tên)'
    list_select_related = ('id_user', 'id_category', 'id_brand')
    ordering = ('-created_at', '-id')

    @admin.display(description='Hình')
    def hinh(self, obj):
        if obj.images:
            return format_html(
                '<img src="{}products/{}" style="width:60px; height:60px; object-fit:cover;">',
                settings.MEDIA_URL, obj.images[0],
            )
        return '-'

    @admin.display(description='Member', ordering='id_user__username')
    def member(self, obj):
        ten = f"{obj.id_user.first_name} {obj.id_user.last_name}".strip()
        return f"{obj.id_user.username} ({ten})" if ten else obj.id_user.username

    @admin.display(description='Trạng thái', ordering='status')
    def trang_thai(self, obj):
        if obj.status == 1:
            return f"Sale {obj.sale}%"
        return "New"

    def delete_model(self, request, obj):
        xoa_hinh_san_pham(obj)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for product in queryset:
            xoa_hinh_san_pham(product)
        super().delete_queryset(request, queryset)
admin.site.register(Product, ProductAdmin)


# ===== History mua hang =====
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'id_user', 'price', 'created_at')
    list_display_links = ('id', 'name')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'id_user__username')
    list_select_related = ('id_user',)
    readonly_fields = ('id_user', 'name', 'email', 'phone', 'price', 'created_at')

    # lich su mua hang chi de xem, khong cho them / sua tay
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
admin.site.register(History, HistoryAdmin)
