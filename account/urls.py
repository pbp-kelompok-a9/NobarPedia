from django.urls import path
import account.views as views 

app_name = 'urls'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('register', views.register_user, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('show_user', views.show_user, name='show_user'),
    path('edit_profile/<int:id>', views.edit_profile, name='edit_profile'),
]
