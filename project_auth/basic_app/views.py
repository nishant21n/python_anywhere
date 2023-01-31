from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

def index(r):
    return render(r, 'basic_app/index.html')


@login_required
def user_logout(r):
    logout(r)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(r):
    return HttpResponse("You are logged in, Nice!")

def register(r):

    registered = False

    if r.method == "POST":
        user_form = UserForm(data=r.POST)# username,password
        profile_form = UserProfileInfoForm(data=r.POST)#profile_pic

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save() # saving username to DB
            user.set_password(user.password)
            user.save() # saving user with HASH password

            profile = profile_form.save(commit=False)
            profile.user = user # user from model.py, profile_pic save with user.

            if 'profile_pic' in r.FILES: # # profile_pic from forms.py
                profile.profile_pic = r.FILES['profile_pic']
                # profile_pic from model. saving to DB

            profile.save()

            registered = True

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(r, "basic_app/register.html",
                  {'user_form': user_form,
                   'registered': registered,
                   'profile_form': profile_form})

def user_login(r):

    if r.method == 'POST':
        username = r.POST.get('username') # name = username from login.html
        password = r.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(r, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not Active")
        else:
            print("Someone tried tp login and faild!")
            print(f"Username: {username} and password: {password}")
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(r, "basic_app/login.html", {})

