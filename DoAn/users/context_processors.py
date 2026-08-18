from .models import User


def custom_auth(request):
    """
    Bơm biến `user` vào mọi template, dựa trên session['user_id'],
    thay thế cho request.user mặc định của Django (chỉ dùng cho auth.User).
    """
    user_id = request.session.get("user_id")
    user = None
    if user_id:
        user = User.objects.filter(id=user_id).first()

    return {
        "custom_user": user,
    }