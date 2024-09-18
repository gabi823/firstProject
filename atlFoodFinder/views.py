from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


# Create your views here.
def login(request):
    return render(request, 'atlFoodFinder/login.html')

def profile_page(request):
    return render(request, 'atlFoodFinder/profile_page.html')
def favorites(request):
    return render(request, 'atlFoodFinder/favorites.html')