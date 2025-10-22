from django.urls import path, include
from review.views import show_reviews, create_review, edit_review, delete_review


app_name = 'review'

urlpatterns =[
    path('create_review/', create_review, name='create_review'),
    path('review/<uuid:nobar_spot_id>', show_reviews, name='show_reviews'),
    path('review/<uuid:id>/update', edit_review, name='edit_review'),
    path('review/<uuid:id>/delete', delete_review, name='delete_review'),
]