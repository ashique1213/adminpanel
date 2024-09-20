from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout


@never_cache
def loginpage(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_panel')
        else:
            return render(request,'home.html')
        
    error_message= None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('admin_panel')
            else:
                return redirect("home")
        else:
            error_message=("Username or Password Incorrect!!!")
    return render(request, "login.html",{'error_message':error_message})


@never_cache
def homepage(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            return render(request, 'home.html')
        else:
            return redirect('admin_panel')  
    return redirect('login')  

@never_cache
def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')
