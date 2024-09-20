from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Create a new user
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            login(request, user)  # Automatically log in the user
            return redirect('atlFoodFinder:show_map')  # Redirect to show_map page
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'atlFoodFinder/create_account.html')

def profile_page(request):
    return render(request, 'atlFoodFinder/profile_page.html')
def favorites(request):
    return render(request, 'atlFoodFinder/favorites.html')

@login_required
def show_map(request):
    return render(request, 'atlFoodFinder/show_map.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('atlFoodFinder:show_map')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect ('atlFoodFinder:show_map')
        else:
            return render(request, 'atlFoodFinder/login.html', {'message': 'Invalid username or password'})

    return render(request, 'atlFoodFinder/login.html')
