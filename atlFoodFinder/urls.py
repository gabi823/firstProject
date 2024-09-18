from django.urls import path

from . import views

app_name = "atlFoodFinder"
urlpatterns = [
    path('map/', views.show_map, name='show_map'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('favorites/', views.favorites, name='favorites'),
]