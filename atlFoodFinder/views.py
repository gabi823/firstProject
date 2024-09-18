from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
def login(request):
    return render(request, 'atlFoodFinder/login.html')

def profile_page(request):
    return render(request, 'atlFoodFinder/profile_page.html')
def favorites(request):
    return render(request, 'atlFoodFinder/favorites.html')

def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Create a new user
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return redirect('/')  # Redirect to home or the login page if accessed via GET


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Logged in successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password'})

    return redirect('/')  # Redirect to home or the login page if accessed via GET