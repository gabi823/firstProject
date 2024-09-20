from django.urls import path
from . import views

app_name = "atlFoodFinder"
urlpatterns = [
    path('', views.login_user, name='home'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('favorites/', views.favorites, name='favorites'),
    path('create_account/', views.create_account, name='create_account'),
    path('login/', views.login_user, name='login_user'),
    path('show_map/', views.show_map, name='show_map'),
    path('logout/', views.logout_user, name='logout_user'),
]