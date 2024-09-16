from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404

@never_cache
def admin_panel(request):
    if request.user.is_authenticated:
        return render(request, "admin.html")
    return render(request,'login.html')

@never_cache
def userinfo(request):
    if request.user.is_authenticated:
        query = request.GET.get('search', '')  
        if query:
            all_users = User.objects.filter(is_superuser=False).filter(
                username__icontains=query) | User.objects.filter(is_superuser=False).filter(email__icontains=query)
        else:
            all_users = User.objects.filter(is_superuser=False)
        return render(request, 'userinfo.html', {'all_users': all_users})
    return render(request,'login.html')

@never_cache
def adduser(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            uname = request.POST.get('username')
            email = request.POST.get('email')
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')

            if pass1 != pass2:
                messages.error(request, "Passwords do not match.")
                return redirect('adduser')
            
            if len(pass1) < 5:
                messages.error(request, "Password must be at least 5 characters long.")
                return redirect('adduser')
            
            if ' ' in pass1 or len(pass1.strip()) == 0:
                messages.error(request, "Password cannot contain spaces or be empty.")
                return redirect('adduser')

            if ' ' in uname or len(uname.strip()) == 0:
                messages.error(request, "Username cannot contain spaces or be empty.")
                return redirect('adduser')
        
            if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already taken.")
                return redirect('adduser')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect('adduser')
            
            User.objects.create_user(username=uname, email=email, password=pass1)
            messages.success(request, "User added successfully!")
            return redirect('adduser')  

        return render(request, 'adduser.html')
    return render(request,'login.html')

@never_cache
def deleteuser(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('userinfo')  
    

@never_cache
def edituser(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            uname = request.POST.get('username')
            email = request.POST.get('email')
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            
            if ' ' in uname or len(uname.strip()) == 0:
                messages.error(request, "Username cannot contain spaces or be empty.")
                return redirect('edituser',user_id=user.id)
            
            if pass1 and pass1 != pass2:
                messages.error(request, "Passwords do not match.")
                return redirect('edituser', user_id=user.id)
            
            if User.objects.filter(username=uname).exclude(id=user.id).exists():
                messages.error(request, "Username already taken.")
                return redirect('edituser', user_id=user.id)
            
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, "Email already registered.")
                return redirect('edituser', user_id=user.id)
            
            user.username = uname
            user.email = email
            if pass1:
                user.set_password(pass1)
            user.save()
            
            messages.success(request, "User updated successfully!")
            return redirect('userinfo') 

        return render(request, 'edit_user.html', {'user': user})
    
    return render(request,'login.html')


def logoutadmin(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')