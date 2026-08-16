from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])

            # Gán quyền
            user.is_superuser = False
            user.is_staff = False

            user.save()
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            request.session["user_id"] = form.user.id
            return redirect("index")
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})

def custom_logout(request):
    logout(request)
    return redirect('login')