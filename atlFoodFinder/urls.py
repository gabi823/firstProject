from django.urls import path
from . import views

app_name = "atlFoodFinder"
urlpatterns = [
    path('profile_page/', views.profile_page, name='profile_page'),
    path('favorites/', views.favorites, name='favorites'),
    path('/login/create_account/', views.create_account, name='create_account'),
    path('login/', views.login_user, name='login_user'),

    path('show_map/', views.show_map, name='show_map'),
]