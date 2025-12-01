from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from account.forms import AdminUserEditForm, CustomUserCreationForm, CustomUserEditForm

from account.models import Profile
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
import json

'''
Note: 
admin punya 3 permission: 
auth.view_user
auth.delete_user 
auth.change_user
'''

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # cek apakah user adalah admin menggunakan permission
            if not user.has_perm('auth.view_user'):                
                response = HttpResponseRedirect(reverse("homepage:show_homepage"))
            else:
                response = HttpResponseRedirect(reverse("account:account_admin_dashboard"))
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
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile updated successfully!')
            return redirect('account:view_profile', id=id)
    else:
        form = CustomUserEditForm(instance=user)
    context = {'form': form }
    return render(request, "edit_profile.html", context)
  
@login_required(login_url='/account/login')
# @csrf_exempt
def delete_profile(request, id):
    # Hanya dirinya sendiri atau ADMIN yg boleh delete
    if not request.user.has_perm('auth.delete_user') and request.user.id != id:
        return HttpResponseRedirect(reverse('homepage:show_homepage'))

    user_to_delete = get_object_or_404(User, pk=id)
    is_admin = request.user.has_perm('auth.delete_user')

    user_to_delete.delete()

    if is_admin:
        # Kalo admin yang delete, balik ke dashboard admin
        return HttpResponseRedirect(reverse('account:account_admin_dashboard'))
    else:
        # Kalo dirinya sendiri yg delete, arahkan ke login
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
            #messages.success(request, 'Your password was successfully updated!')
            return redirect('account:edit_profile', id=id)
        #else:
            #messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user)

    return render(request, 'change_password.html', {'form': form})

@login_required(login_url='/account/login')
def show_user(request):
    return JsonResponse(data=[{'msg':'this is user page'}], safe=False)

@login_required(login_url='/account/login')
def account_admin_dashboard(request):
    if not request.user.has_perm('auth.view_user'):
        return HttpResponseRedirect(reverse('homepage:show_homepage'))
        
    users = User.objects.all()
    context = {'users': users}
    return render(request, "account_admin_dashboard.html", context)

@login_required(login_url='/account/login')
def admin_edit_profile(request, id):
    if not request.user.has_perm('auth.change_user'):
        return HttpResponseRedirect(reverse('homepage:show_homepage'))

    user_to_edit = get_object_or_404(User, pk=id)
    
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, request.FILES, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile updated successfully!')
            return redirect('account:account_admin_dashboard')
    else:
        form = AdminUserEditForm(instance=user_to_edit)

    context = {'form': form, 'user_to_edit': user_to_edit}
    return render(request, "admin_edit_profile.html", context)


# API for FLUTTER APP
@csrf_exempt
def login_flutter(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Login status successful.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login successful!"
                # Add other data if you want to send data to Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, account is disabled."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, please check your username or password."
        }, status=401)


@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
    

@csrf_exempt
def logout_flutter(request):
    username = request.user.username
    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)

@login_required
def current_user_id(request):
    is_admin = request.user.has_perm('auth.delete_user')  
    return JsonResponse({
        "id": request.user.id,
        "username": request.user.username,
        "is_admin": is_admin,
    })
        
def view_profile_flutter(request, id):
    user = get_object_or_404(User, pk=id)
    profile = getattr(user, "profile", None)
    
    show_update_button = False
    if (request.user.id == id):
        show_update_button = True
    # print(getattr(profile, "profile_picture", "").url)
    try:
        profile_picture_url = getattr(profile, "profile_picture", "")
        if profile_picture_url:
            # print(profile_picture_url.url)
            profile_picture_url = profile_picture_url.url # type: ignore
        
        return JsonResponse({
            "username": user.username,
            "email": user.email,
            "fullname": getattr(profile, "fullname", ""),
            "bio": getattr(profile, "bio", ""),
            "profile_picture_url": profile_picture_url,
            "show_update_button": show_update_button
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Error on fetching profile"
        }, status=401)

@csrf_exempt
def edit_profile_flutter(request, id):
    if request.user.id != id:
        return JsonResponse({
            "status": False,
            "message": "your not allowed to edit other profiles dawg"
        }, status=403)
        
    user = get_object_or_404(User, pk=id)
    
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "status": True,
                "message": "User profile updated successfully!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": form.errors
            }, status=400)
    else:
        return JsonResponse({
            "status": False,
            "message": "use POST method please"
        }, status=405)
        
 
@csrf_exempt
def change_password_flutter(request, id):
    if request.user.id != id:
        return JsonResponse({
            "status": False,
            "message": "yore not allowed to change other people's passwords."
        }, status=403)

    user = get_object_or_404(User, pk=id)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            
            return JsonResponse({
                "status": True,
                "message": "Password changed successfully!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": form.errors
            }, status=400)
    return JsonResponse({
        "status": False,
        "message": "Use POST method please"
    }, status=405)
    
    
@csrf_exempt
def delete_profile_flutter(request, id):
    # Hanya dirinya sendiri atau ADMIN yg boleh delete
    if request.user.id != id:
        return JsonResponse({
            "status": False,
            "message": "yore not allowed to change other people's passwords."
        }, status=403)

    user_to_delete = get_object_or_404(User, pk=id)

    user_to_delete.delete()

    return JsonResponse({
        "status": True,
        "message": "Account has been successfully deleted."
    }, status=403)
