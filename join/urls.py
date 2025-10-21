from django.urls import path
from join.views import tes, post_join, get_join_list, get_join_record, update_join, delete_join

app_name = 'join'

urlpatterns = [
    path('', tes),
    path('post/', post_join),
    path('get/', get_join_list),
    path('get/<uuid:id>/', get_join_record),
    path('update/<uuid:id>/', update_join),
    path('delete/<uuid:id>/', delete_join),
]
