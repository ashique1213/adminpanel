from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404


def admin_panel(request):
    return render(request,'admin.html')

def userinfo(request):
    all_users = User.objects.filter(is_superuser=False)
    return render(request, 'userinfo.html', {'all_users': all_users})


def adduser(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
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


def deleteuser(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        print(user)
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('userinfo')  
    


def edituser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
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
