from django.urls import path
from join.views import tes

app_name = 'join'

urlpatterns = [
    path('', tes)
]
