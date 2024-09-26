import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout
from django import forms
from .models import FavoriteRestaurant



# Create your views here.

@login_required
def add_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data.get('place_id')
        name = data.get('name')
        rating = data.get('rating')
        address = data.get('address')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Check if the restaurant is already favorited by the user
        if FavoriteRestaurant.objects.filter(user=request.user, place_id=place_id).exists():
            return JsonResponse({'status': 'error', 'message': 'This restaurant is already in your favorites.'})

        # Add the restaurant to the user's favorites
        favorite = FavoriteRestaurant(
            user=request.user,
            name=name,
            place_id=place_id,
            rating=rating,
            address=address,
            latitude=latitude,
            longitude=longitude
        )
        favorite.save()

        return JsonResponse({'status': 'success', 'message': 'Restaurant has been added to favorites.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def remove_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data.get('place_id')

        FavoriteRestaurant.objects.filter(user=request.user, place_id=place_id).delete()

        return JsonResponse({'status': 'success', 'message': 'Restaurant has been removed from favorites.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def get_favorites(request):
    favorites = FavoriteRestaurant.objects.filter(user=request.user)
    favorite_list = []
    for favorite in favorites:
        favorite_list.append({
            'name': favorite.name,
            'place_id': favorite.place_id,
            'rating': favorite.rating,
            'address': favorite.address,
            'latitude': favorite.latitude,
            'longitude': favorite.longitude
        })
    return JsonResponse({'status': 'success', 'favorites': favorite_list})

class CustomPasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")

        return cleaned_data

@login_required
def profile_page(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password1')
            user = request.user
            user.set_password(new_password)
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('atlFoodFinder:profile_page')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm()

    return render(request, 'atlFoodFinder/profile_page.html',{
        'user': request.user,
        'form': form,
    })

def logout_user(request):
    logout(request)
    return redirect('atlFoodFinder:login_user')

def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        print(f"First Name: {first_name}, Last Name: {last_name}")

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
        print(f"Username: {username}, Password: {password}")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f'User {username} authenticated successfully')
            return JsonResponse({'status': 'success', 'redirect_url': '/show_map/'})
        else:
            print("Invalid credentials")
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password'})
    return render(request, 'atlFoodFinder/login.html')
def reviews(request):
    return render(request, 'atlFoodFinder/reviews.html')