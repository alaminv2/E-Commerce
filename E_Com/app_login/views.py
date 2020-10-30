# a@123456
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from app_login.forms import signUpForm, profileForm
from app_login.models import Profile, User


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# Create your views here.


def signUpView(request):
    form = signUpForm()
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            form = signUpForm()
            messages.success(request, 'Account Creatd Successfully.....')
            return HttpResponseRedirect(reverse('app_login:login'))

    return render(request, 'app_login/sign_up_page.html', context={'form': form})


def loginView(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('app_shop:home'))

    return render(request, 'app_login/login_page.html', context={'form': form})


@login_required
def logoutView(request):
    logout(request)
    messages.warning(request, 'You are Logged Out.....!')
    return HttpResponseRedirect(reverse('app_shop:home'))


@login_required
def profileView(request):
    profile_obj = Profile.objects.get(user=request.user)

    form = profileForm(instance=profile_obj)
    if request.method == 'POST':
        form = profileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            form = profileForm(instance=profile_obj)
            messages.success(request, 'Profile Successfully Updated......!')

    return render(request, 'app_login/profile_page.html', context={'form': form})
