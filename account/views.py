from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from account.forms import CustomUserCreationForm, CustomUserEditForm

from account.models import Profile
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
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
            response = HttpResponseRedirect(reverse("homepage:show_homepage"))
            # response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def register_user(request):
    form = CustomUserCreationForm()
    # if request.method == "POST":
    #     form = CustomUserCreationForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         user = form.save()
    #         user.save()
    #         messages.success(request, 'Your account has been successfully created!')
    #         return redirect('account:login')
    
    context = {'form': form}
    return render(request, 'register.html', context)
  
def register_ajax(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return JsonResponse({"success": True, "message": "Account created successfully!"})
        else:
            # Return form errors in JSON
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)
  
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('account:login'))
    # response.delete_cookie('last_login')
    return response

def view_profile(request, id):
    show_update_button = False
    if (request.user.id == id):
        show_update_button = True
        
    user = get_object_or_404(User, pk=id)
    context = {"user" : user, "show_update_button": show_update_button}
    return render(request, "view_profile.html", context)

@login_required(login_url='/account/login')
def edit_profile(request, id):
    if request.user.id != id:
        # print('ga boleh edit punya orang  lain bro', request.user.id, " ", id)
        return HttpResponseRedirect(reverse('homepage:show_homepage'))
    user = get_object_or_404(User, pk=id)
    form = CustomUserEditForm(request.POST or None, instance=user)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('account:view_profile', id=id)
    context = {'form': form }
    return render(request, "edit_profile.html", context)
  
@login_required(login_url='/account/login')
@csrf_exempt
def delete_profile(request, id):
  user = get_object_or_404(User, pk=id)
  user.delete()
  return HttpResponseRedirect(reverse('account:login'))

# @login_required(login_url='/account/login')
# def delete_profile_from_admin(request, id):
#   if not request.user.is_staff:
#     return HttpResponseRedirect(reverse('account:admin'))
#   user = get_object_or_404(User, pk=id)
#   user.delete()
#   return HttpResponseRedirect(reverse('account:admin'))
  
@login_required(login_url='/account/login')
def change_password(request, id):
    if request.user.id != id:
        print('ga boleh edit punya orang  lain bro', request.user.id, " ", id)
        return HttpResponseRedirect(reverse('homepage:show_homepage'))
    
    user = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # agar user ga ke logout otomatis, langsung update session dengan password yg baru
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account:edit_profile', id=id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user)

    return render(request, 'change_password.html', {'form': form})

@login_required(login_url='/account/login')
def show_user(request):
    return JsonResponse(data=[{'msg':'this is user page'}], safe=False)
