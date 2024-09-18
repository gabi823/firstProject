from django.urls import path

from . import views

app_name = "atlFoodFinder"
urlpatterns = [
    path('login/', views.login, name='login'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('favorites/', views.favorites, name='favorites'),
]