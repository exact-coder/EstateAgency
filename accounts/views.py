from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout as django_logout, login as django_login

from accounts.models import User

# Create your views here.

def registration(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST' and request.FILES['image']:
            method_dict = request.POST.copy()
            name = method_dict.get('name')
            phone = method_dict.get('phone')
            email = method_dict.get('email')
            address = method_dict.get('address')
            password1 = method_dict.get('password1')
            password2 = method_dict.get('password2')
            image = request.FILES['image']

            email.lower()
            email_exists = User.objects.filter(email = email)
            if not email_exists:
                if password1 == password2:
                    user = User.objects.create_user(first_name = name, phone = phone,email = email, address = address , password = password2, image = image)
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Registation Done! You can login now')
                    return redirect('login')
                else:
                    messages.success(request, 'Password did not matched!')
            else:
                messages.success(request, 'Email already taken!')
    return render(request, 'accounts/registration.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            email.lower()
            user = authenticate(request, email = email, password = password)
            if user is not None:
                django_login(request,user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid Email or Password')
    return render(request, 'accounts/login.html')

def logout(request):
    django_logout(request)
    return redirect('login')