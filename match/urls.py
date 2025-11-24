from django.urls import path
from . import views
from .models import Competition, Match, Player
from .forms import CompetitionForm, MatchForm, PlayerForm

app_name = 'match'

urlpatterns = [
    path('home/', views.match_main, name="match_main"),

    path('api/match/post/create_competition/', views.BasicMatchAPIView.as_view(
        model_class=Competition,
        form_class=CompetitionForm,
        opt='c'
    ), name='api_create_competition'),

    path('api/match/post/create_match/', views.BasicMatchAPIView.as_view(
        model_class=Match,
        form_class=MatchForm,
        opt='c'
    ), name='api_create_match'),

    path('api/match/post/create_player/', views.BasicMatchAPIView.as_view(
        model_class=Player,
        form_class=PlayerForm,
        opt='c'
    ), name='api_create_player'),


    path('api/match/post/update_competition/<str:id>/', views.BasicMatchAPIView.as_view(
        model_class=Competition,
        form_class=CompetitionForm,
        opt='u'
    ), name='api_update_competition'),

    path('api/match/post/update_match/<str:id>/', views.BasicMatchAPIView.as_view(
        model_class=Match,
        form_class=MatchForm,
        opt='u'
    ), name='api_update_match'),

    path('api/match/post/update_player/<str:id>/', views.BasicMatchAPIView.as_view(
        model_class=Player,
        form_class=PlayerForm,
        opt='u'
    ), name='api_update_player'),


    path('api/match/post/delete_competition/<str:id>/', views.BasicMatchAPIView.as_view(
        model_class=Competition,
        opt='d'
    ), name='api_delete_competition'),

    path('api/match/post/delete_match/<str:id>/', views.BasicMatchAPIView.as_view(
        model_class=Match,
        opt='d'
    ), name='api_delete_match'),

    path('api/match/post/delete_player/<str:id>/', views.BasicMatchAPIView.as_view(
        model_class=Player,
        opt='d'
    ), name='api_delete_player'),


    path('api/match/post/read_competition/<str:id>/', views.BasicMatchAPIView.as_view(
        model_class=Competition,
        opt='r'
    ), name='api_read_competition'),

    path('api/match/post/read_match/<str:id>/', views.BasicMatchAPIView.as_view(
        model_class=Match,
        opt='r'
    ), name='api_read_match'),

    path('api/match/post/read_player/<str:id>/', views.BasicMatchAPIView.as_view(
        model_class=Player,
        opt='r'
    ), name='api_read_player'),


    path('api/match/post/read_all_competition/', views.BasicMatchAPIView.as_view(
        model_class=Competition,
        opt='ra'
    ), name='api_read_all_competition'),

    path('api/match/post/read_all_match/', views.BasicMatchAPIView.as_view(
        model_class=Match,
        opt='ra'
    ), name='api_read_all_match'),

    path('api/match/post/read_all_player/', views.BasicMatchAPIView.as_view(
        model_class=Player,
        opt='ra'
    ), name='api_read_all_player'),


]
