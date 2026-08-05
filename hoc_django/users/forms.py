from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Xóa dòng ghi chú mặc định của username
        self.fields['username'].help_text = ''

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get("password")
        confirm_pw = cleaned_data.get("confirm_password")

        if pw and confirm_pw and pw != confirm_pw:
            raise forms.ValidationError("Mật khẩu không khớp.")