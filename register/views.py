# locallibrary/register/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Get the new user info and set the group for this user to LibraryMember
            lib_group = Group.objects.get(name='LibraryMember')
            user.groups.add(lib_group)
            user.save()

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})
