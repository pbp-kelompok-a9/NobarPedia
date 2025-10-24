from django.urls import path
from join.views import show_join, post_join, get_join, update_join, delete_join

app_name = 'join'

urlpatterns = [
    path('', show_join, name='show_join'),
    path('post/<uuid:nobar_place_id>/', post_join, name='post_join'),
    path('get/', get_join, name='get_join'),
    path('update/<uuid:id>/', update_join, name='update_join'),
    path('delete/<uuid:id>/', delete_join, name='delete_join'),
]
