from django.urls import path

from . import views

app_name = "atlFoodFinder"
urlpatterns = [path('map/', views.show_map, name='show_map'),]