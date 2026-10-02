from django.contrib import messages
from django.shortcuts import redirect


def la_admin(user):
    return user.is_staff or user.is_superuser


DUONG_DAN_BO_QUA = ("/static/", "/media/", "/ckeditor/", "/users/logout/")


class PhanQuyenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        user = request.user

        if user.is_authenticated and not path.startswith(DUONG_DAN_BO_QUA):
            vao_admin = path.startswith("/admin/")

            if vao_admin and not la_admin(user):
                messages.error(request, "Bạn không có quyền vào trang quản trị.")
                return redirect("index")

            if not vao_admin and la_admin(user):
                messages.warning(request, "Tài khoản admin chỉ được dùng để truy cập trang quản trị.")
                return redirect("admin:index")

        return self.get_response(request)
