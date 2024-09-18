from django.urls import path
from .views import create_account, login_user

from . import views

app_name = "atlFoodFinder"
urlpatterns = [
    path('login/', views.login, name='login'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('favorites/', views.favorites, name='favorites'),
    path('create_account/', create_account, name='create_account'),
    path('login/', login_user, name='login_user'),
]