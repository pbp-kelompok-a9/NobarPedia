from django.urls import path
from homepage.views import show_homepage, create_spot,show_spot

app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage'),
    path('create-spot/',create_spot, name='create_spot'),
    path('spot/<str:id>/',show_spot,name='show_spot'),
]