import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .forms import CustomPasswordChangeForm
from django.contrib.auth import logout
from django import forms
from .models import FavoriteRestaurant

# Create your views here.

@login_required
def add_favorite(request):
    if request.method == 'POST':
        try:
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

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

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

@login_required
def profile_page(request):
    form = CustomPasswordChangeForm()
    success_message = None
    error_message = None

    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password1')
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            success_message = 'Your password has been successfully updated!'
            return render(request, 'atlFoodFinder/profile_page.html', {
                'user': request.user,
                'form': form,
                'success_message': success_message,
                'error_message': error_message,
            })
        else:
            error_message = 'Your password change was not valid. Try again!'
    else:
        form = CustomPasswordChangeForm()

        # Render the profile page with the form
    return render(request, 'atlFoodFinder/profile_page.html', {
        'user': request.user,
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
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

        errors = {}

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            errors['username_error'] = 'This username is already in use.'

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors['email_error'] = 'This email is already in use.'

        if errors:
            # If errors exist, re-render the form with error messages and previously entered data
            return render(request, 'atlFoodFinder/create_account.html', {
                'errors': errors,
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })

        # Create a new user if no issues
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

    return render(request, 'atlFoodFinder/create_account.html', {'errors': {}})


@login_required
def favorites(request):
    # Get all favorite restaurants for the current user
    favorites = FavoriteRestaurant.objects.filter(user=request.user)
    return render(request, 'atlFoodFinder/show_map.html', {'favorites': favorites})

@login_required
def show_map(request):
    favorited_place_ids = FavoriteRestaurant.objects.filter(user=request.user).values_list('place_id', flat=True)
    return render(request, 'atlFoodFinder/show_map.html', {
        'favorited_place_ids': list(favorited_place_ids)
    })

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
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            # Get new password and update the user’s password
            new_password1 = form.cleaned_data['new_password1']
            request.user.set_password(new_password1)
            request.user.save()

            # Update session hash to keep the user logged in
            update_session_auth_hash(request, request.user)

            # Redirect to a success page after the password change
            return redirect('password_change_done')  # Make sure this URL exists
    else:
        form = CustomPasswordChangeForm()

    return render(request, 'change_password.html', {'form': form})