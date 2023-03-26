from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Profile

# Create your views here.


def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj1 = User.objects.filter(email=email)

        print(request.POST)

        if not user_obj1.exists():
            messages.warning(request, "Account does not exist")
            return HttpResponseRedirect(request.path_info)
        else:
            if not user_obj1[0].profile.is_email_verified():
                messages.warning(request, "Email is not verified.")
                HttpResponseRedirect(request.path_info)

            else:
                user_obj1 = User.authenticate(email=email, password=password)
                if user_obj1:
                    login(request, user_obj1)
                    return redirect("/")

            messages.warning(request, 'Invalid Credentials')
            return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')


def register_page(request):

    if request.user.is_authenticated:
        # return HttpResponseRedirect('/accounts/myprofile')
        pass

    # change this to elif (down)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        password = request.POST.get('password')

        user_obj1 = User.objects.filter(email=email)
        user_obj2 = User.objects.filter(username=username)

        if user_obj1.exists():
            messages.warning(request, "Email already exists")
            return HttpResponseRedirect(request.path_info)

        elif user_obj2.exists():
            messages.warning(request, "Username already exists")
            return HttpResponseRedirect(request.path_info)

        else:
            print(email)

            user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=username)
            user_obj.set_password(password)
            user_obj.save()

            messages.success(request, 'An email has been sent to verify your identity')
            return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')


def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()

        messages.success(request, "Your email has been verified you can login now!")
        return HttpResponseRedirect('/accounts/login')

    except Exception as e:
        print(e)
        return HttpResponseRedirect('/misc/unknownerror.html')
