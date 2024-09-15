from django.urls import path

from . import views

app_name = "atlFoodFinder"
urlpatterns = [
    path('map/', views.show_map, name='show_map'),
    path('welcome/', views.welcome, name='welcome'),
    path('login/', views.login, name='login'),
    path('create_account/', views.createaccount, name='create_account'),
]