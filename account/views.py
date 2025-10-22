from django.contrib.auth.forms import AuthenticationForm
from account.forms import CustomUserCreationForm, CustomUserEditForm

from account.models import Profile
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers
import datetime
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("account:show_user"))
            # response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)

    context = {'form': form}
    return render(request, 'login.html', context)

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('account:login')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'register.html', context)
  
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('account:login'))
    # response.delete_cookie('last_login')
    return response

@login_required(login_url='/account/login')
def edit_profile(request, id):
    user = get_object_or_404(User, pk=id)
    form = CustomUserEditForm(request.POST or None, instance=user)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('account:show_user')

    context = {
        'form': form
    }

    return render(request, "edit_profile.html", context)

@login_required(login_url='/account/login')
def show_user(request):
    return JsonResponse(data=[{'msg':'this is user page'}], safe=False)
