from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.urls import reverse

def list_users(request):
    users = User.objects.all()
    return render(request, 'users/list_users.html', {'users': users})


def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        User.objects.create(username=username, email=email)
        return redirect(('list_users'))
    return render(request, 'users/add_user.html')

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        return redirect('list_users')
    return render(request, 'users/edit_user.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('list_users')