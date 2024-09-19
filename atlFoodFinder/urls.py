from django.urls import path

from . import views

app_name = "atlFoodFinder"
urlpatterns = [
    path('', views.show_map, name='welcome'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('favorites/', views.favorites, name='favorites'),
    path('/login/create_account/', views.createaccount, name='create_account'),
    path('login/', views.login, name='login'),

    path('map/', views.show_map, name='show_map'),
]