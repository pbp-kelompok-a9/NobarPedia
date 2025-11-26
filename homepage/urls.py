from django.urls import path
from homepage.views import show_homepage, create_spot,show_spot
from homepage.views import delete_spot, show_json, edit_spot, get_user_nobar_spots

app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage'),
    path('create-spot/',create_spot, name='create_spot'),
    path('spot/<str:id>/',show_spot,name='show_spot'),
    path('spot/<uuid:id>/delete', delete_spot,name='delete_spot'),
    path('json/', show_json, name='show_json'),
    path('spot/<uuid:id>/edit', edit_spot, name='edit_spot'),
    path('user-spots-json/', get_user_nobar_spots, name='get_user_nobar_spots'),
]
