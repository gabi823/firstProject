from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
def create_account(request):
    return render(request, 'atlFoodFinder/create_account.html')
def profile_page(request):
    return render(request, 'atlFoodFinder/profile_page.html')
def favorites(request):
    return render(request, 'atlFoodFinder/favorites.html')

def show_map(request):
    return render(request, 'atlFoodFinder/show_map.html')

def create_account_action(request):
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

    return render(request, 'atlFoodFinder/create_account.html')


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

    return render(request, 'atlFoodFinder/login.html')