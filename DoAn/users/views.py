from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm


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
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect("login")


@login_required
def index(request):
    return render(request, 'index.html')



@login_required
def account_update(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Update successfully!")
            return redirect("account_update")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "account.html", {"form": form})


@login_required
def my_product(request):
    return render(request, "my_product.html")


@login_required
def add_product(request):
    return render(request, "add_product.html")
