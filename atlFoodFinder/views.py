from django.shortcuts import render

# Create your views here.
def show_map(request):
    return render(request, 'atlFoodFinder/show_map.html')

def profile_page(request):
    return render(request, 'atlFoodFinder/profile_page.html')
def favorites(request):
    return render(request, 'atlFoodFinder/favorites.html')