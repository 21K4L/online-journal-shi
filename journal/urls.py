from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/<int:pk>/rate/', views.add_rating, name='add_rating'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('create/', views.create_article, name='create_article'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('users-guide/', views.users_guide, name='users_guide'),
    path('judges-guide/', views.judges_guide, name='judges_guide'),
]
