from django import forms
from django.core.exceptions import ValidationError
from . models import CustomerUser
from django.core.validators import FileExtensionValidator

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=10)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'password', 'confirm_password', 'avatar','first_name','last_name', 'id_country']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomerUser.objects.filter(username=username).exists():
            raise ValidationError("Username đã tồn tại.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomerUser.objects.filter(email=email).exists():
            raise ValidationError("Email đã được sử dụng.")
        return email
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 1024 * 1024: 
                raise ValidationError("Kích thước ảnh không được vượt quá 1MB.")
            if not avatar.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError("Chỉ chấp nhận các định dạng ảnh: .jpg, .jpeg, .png.")
        return avatar

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Mật khẩu xác nhận không khớp.")