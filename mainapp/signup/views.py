from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def sign(request):
    if request.method =='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if pass1!=pass2:
            return HttpResponse("password issue")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            print(uname,email,pass1,pass2)
            return redirect('login')
    
    return render(request,'signup.html')