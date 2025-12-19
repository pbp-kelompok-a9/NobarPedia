from django.urls import path
from homepage.views import show_homepage, create_spot,show_spot, proxy_image, json_spots
from homepage.views import delete_spot, edit_spot, get_user_nobar_spots, create_spot_flutter
from homepage.views import delete_spot_flutter, edit_spot_flutter, json_my_spot
app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage'),
    path('create-spot/',create_spot, name='create_spot'),
    path('spot/<str:id>/',show_spot,name='show_spot'),
    path('spot/<uuid:id>/delete', delete_spot,name='delete_spot'),
    path('json/', json_spots, name='json_spots'),
    path('json-mine/', json_my_spot, name='json_mine'),
    path('spot/<uuid:id>/edit', edit_spot, name='edit_spot'),
    path('user-spots-json/', get_user_nobar_spots, name='get_user_nobar_spots'),
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-spot-flutter/',create_spot_flutter,name='create-spot-flutter'),
    path('delete-spot-flutter/<uuid:id>/',delete_spot_flutter,name='delete-spot-flutter'),
    path('edit-spot-flutter/<uuid:id>/', edit_spot_flutter, name='edit-spot-flutter'),
]