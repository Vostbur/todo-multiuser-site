from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'authentication/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'authentication/signup.html',
                              {'form': UserCreationForm(),
                               'error': 'User already exists. Please choose a new username'})
        else:
            return render(request, 'authentication/signup.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})
# def signup_user(request):
#     error = ''
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             try:
#                 user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
#                 user.save()
#                 login(request, user)
#                 return redirect('home')
#             except IntegrityError:
#                 error = 'User already exists. Please choose a new username'
#         else:
#             error = 'Passwords did not match'
#     return render(request, 'authentication/signup.html', {'form': UserCreationForm(), 'error': error})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'authentication/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'authentication/login.html',
                          {'form': AuthenticationForm(),
                           'error': 'User or password did not match'})
        else:
            login(request, user)
            return redirect('home')
# def login_user(request):
#     error = ''
#     if request.method == 'POST':
#         user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
#         if user:
#             login(request, user)
#             return redirect('home')
#         error = 'User or password did not match'
#     return render(request, 'authentication/login.html', {'form': AuthenticationForm(), 'error': error})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
