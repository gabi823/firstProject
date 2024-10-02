from django.urls import path
from . import views

app_name = "atlFoodFinder"
urlpatterns = [
    path('', views.login_user, name='home'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('favorites/', views.show_map, name='favorites'),
    path('create_account/', views.create_account, name='create_account'),
    path('login/', views.login_user, name='login_user'),
    path('show_map/', views.show_map, name='show_map'),
    path('logout/', views.logout_user, name='logout_user'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/', views.remove_favorite, name='remove_favorite'),
    path('get_favorites/', views.get_favorites, name='get_favorites'),
    path('change-password/', views.change_password, name='change_password'),
]