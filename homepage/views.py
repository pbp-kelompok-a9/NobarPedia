from django.shortcuts import render, redirect, get_object_or_404
from homepage.forms import NobarSpotForm
from homepage.models import NobarSpot
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from join.models import Join_List # Import Join_List
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import json
from django.http import JsonResponse

# Create your views here.
def show_homepage(request):
    nobarSpot_list = NobarSpot.objects.all()
    context={
        'nobarSpot_list' : nobarSpot_list,
        'name': request.user.username,
    }
    return render(request, "homepage.html",context)

@login_required(login_url='/account/login')
def create_spot(request):
    form = NobarSpotForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        spot_entry=form.save(commit=False)
        spot_entry.host = request.user
        spot_entry.save()
        return redirect('homepage:show_homepage')
    
    context = {'form':form}
    return render(request, "create_spot.html", context)

@login_required(login_url='/account/login')
def edit_spot(request, id):
    nobarSpot = get_object_or_404(NobarSpot, pk=id)
    form = NobarSpotForm(request.POST or None, instance=nobarSpot)

    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('homepage:show_homepage')

    context = {
        'form': form
    }

    return render(request, "edit_spot.html", context)

def show_spot(request):
    nobarSpot = get_object_or_404(NobarSpot,pk=id)
    context={
        'nobarSpot' : nobarSpot
    }
    return render(request, "spot_detail.html",context)

@login_required(login_url='/account/login')
def delete_spot(request,id):
    nobarSpot = get_object_or_404(NobarSpot,pk=id)
    nobarSpot.delete()
    return HttpResponseRedirect(reverse('homepage:show_homepage'))

def json_spots(request):
    spot_list = NobarSpot.objects.all()
    data = [
        {
            'id': str(spot.id),
            'name': spot.name,
            'thumbnail': spot.thumbnail,
            'home_team':spot.home_team,
            'away_team' : spot.away_team,
            'date': spot.date,
            'time': spot.time,
            'city': spot.city,
            'address': spot.address,
            'host': spot.host.id,
        }
        for spot in spot_list
    ]
    return JsonResponse(data, safe=False)

@login_required(login_url='/account/login')
def get_user_nobar_spots(request):
    user_nobar_spots = NobarSpot.objects.filter(host=request.user)
    data = [
        {
            'id': str(spot.id),
            'name': spot.name,
            'city': spot.city,
            'time': spot.time.strftime('%H:%M') if spot.time else None,
            'host_id': str(spot.host.id),
            'host_username': spot.host.username,
            'joined_count': spot.join_list_set.count(), # Add joined count
        }
        for spot in user_nobar_spots
    ]
    return JsonResponse(data, safe=False)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_spot_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        name = strip_tags(data.get("name", ""))  # Strip HTML tags
        thumbnail = data.get("thumbnail", "")
        home_team = strip_tags(data.get("home_team", ""))  # Strip HTML tags
        away_team = strip_tags(data.get("away_team", ""))  # Strip HTML tags
        date = data.get("date", "")
        time = data.get("time", "")
        city = strip_tags(data.get("city",""))
        address = strip_tags(data.get("address",""))
        host = request.host
        
        new_spot = NobarSpot(
            name=name, 
            thumbnail = thumbnail,
            home_team=home_team,
            away_team=away_team,
            data = date,
            time=time,
            city=city,
            address=address,
            host=host,
        )
        new_spot.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
