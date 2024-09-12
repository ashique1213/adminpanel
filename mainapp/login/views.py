# from django.shortcuts import render

# # Create your views here.

from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


@never_cache
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    error_message= None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error_message=("Username or Password Incorrect!!!")
    return render(request, "login.html",{'error_message':error_message})


@never_cache
def homepage(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    return redirect('login')

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')
