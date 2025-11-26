from django.urls import path
from join.views import show_join, post_join, get_join, update_join, delete_join, create_join_flutter, update_join_flutter, delete_join_flutter

app_name = 'join'

urlpatterns = [
    path('', show_join, name='show_join'),
    path('post/<uuid:nobar_place_id>/', post_join, name='post_join'),
    path('get/', get_join, name='get_join'),
    path('update/<uuid:id>/', update_join, name='update_join'),
    path('delete/<uuid:id>/', delete_join, name='delete_join'),
    path('create-flutter/', create_join_flutter, name='create_join_flutter'),
    path('update-flutter/<uuid:id>/', update_join_flutter, name='update_join_flutter'),
    path('delete-flutter/<uuid:id>/', delete_join_flutter, name='delete_join_flutter'),
]
