from django.urls import path
import account.views as views 

app_name = 'urls'

urlpatterns = [
    path('/login', views.login, name='login'),
    path('/register', views.register, name='register'),
    path('/logout', views.logout, name='logout'),
    path('/edit_profile/<int:id>', views.edit_profile, name='edit_profile'),
]
