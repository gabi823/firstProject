from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.
def logout_user(request):
    logout(request)
    return redirect('atlFoodFinder:login_user')

@login_required
def profile_page(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('atlFoodFinder:profile_page')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'atlFoodFinder/profile_page.html', {
        'user': request.user,
    })

def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Create a new user
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            login(request, user)  # Automatically log in the user
            return redirect('atlFoodFinder:show_map')  # Redirect to show_map page
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'atlFoodFinder/create_account.html')

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