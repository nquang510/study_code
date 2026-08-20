from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    confirm_password = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}),
    )

    class Meta:
        model = User
        fields = [
            "username", "email", "password", "confirm_password",
            "avatar", "first_name", "last_name", "id_country",
        ]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username đã tồn tại.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email đã tồn tại.")
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            if avatar.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError("Kích thước ảnh không được vượt quá 2MB.")
            if not avatar.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Định dạng ảnh không hợp lệ. Chỉ chấp nhận các định dạng: .jpg, .jpeg, .png.")
        return avatar

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Mật khẩu xác nhận không khớp.")
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    """
    Kế thừa thẳng AuthenticationForm chuẩn của Django. Với AbstractUser,
    việc xác thực (kiểm tra username/password) đã được xử lý đúng chuẩn
    bởi authenticate()/ModelBackend trong AuthenticationForm.clean(),
    nên không cần tự viết lại logic kiểm tra mật khẩu như trước.
    """

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
