from django.urls import path, include
from review.views import show_reviews, create_review, edit_review, delete_review, show_test


app_name = 'review'

urlpatterns =[
    path('', show_test, name="show_test"),
    path('create_review/', create_review, name='create_review'),
    path('review/<uuid:id>', show_reviews, name='show_reviews'),
    path('review/<uuid:id>/update', edit_review, name='edit_review'),
    path('review/<uuid:id>/delete', delete_review, name='delete_review'),
]