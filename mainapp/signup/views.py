from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def sign(request):
    if request.method =='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if pass1!=pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        if len(pass1) < 5:
            messages.error(request, "Password must be at least 5 characters long.")
            return redirect('signup')
        
        if ' ' in pass1 or len(pass1.strip()) == 0:
            messages.error(request, "Password cannot contain spaces or be empty.")
            return redirect('signup')

        if ' ' in uname or len(uname.strip()) == 0:
            messages.error(request, "Username cannot contain spaces or be empty.")
            return redirect('signup')
        
        if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already taken.")
                return redirect('signup')
            
        if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect('signup')
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            print(uname,email,pass1,pass2)
            messages.success(request, "Registered Succesfully...")
            return redirect('signup')
            # return redirect('login')
    
    return render(request,'signup.html')