from django.urls import path
import account.views as views 

app_name = 'urls'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('register', views.register_user, name='register'),
    path('register_ajax', views.register_ajax, name='register_ajax'),
    path('logout', views.logout_user, name='logout'),
    path('show_user', views.show_user, name='show_user'),
    path('view_profile/<int:id>', views.view_profile, name='view_profile'),
    path('edit_profile/<int:id>', views.edit_profile, name='edit_profile'),
    path('change_password/<int:id>', views.change_password, name='change_password'),
    path('delete_profile/<int:id>', views.delete_profile, name='delete_profile'),
    path('admin', views.account_admin_dashboard, name='account_admin_dashboard'),
    path('admin/edit_profile/<int:id>', views.admin_edit_profile, name='admin_edit_profile'),
]
