from django.shortcuts import render, redirect, get_object_or_404
from homepage.forms import NobarSpotForm
from homepage.models import NobarSpot
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Create your views here.
def show_homepage(request):
    nobarSpot_list = NobarSpot.objects.all()
    context={
        'nobarSpot_list' : nobarSpot_list,
        'name': request.user.username,
    }
    return render(request, "homepage.html",context)

def create_spot(request):
    form = NobarSpotForm(request.POST or None)

    if form.is_valid and request.method == "POST":
        form.save()
        return redirect('homepage:show_homepage')
    
    context = {'form':form}
    return render(request, "create_spot.html", context)

def show_spot(request):
    nobarSpot = get_object_or_404(NobarSpot,pk=id)
    context={
        'nobarSpot' : nobarSpot
    }
    return render(request, "spot_detail.html",context)

def delete_spot(request,id):
    nobarSpot = get_object_or_404(NobarSpot,pk=id)
    nobarSpot.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def show_json(request):
    spot_list = NobarSpot.objects.all()
    data = [
        {
            'id': str(spot.id),
            'name': spot.name,
            'thumbnail': spot.thumbnail,
            'home_team':spot.home_team,
            'away_team':spot.away_team,
            'date':spot.date,
            'time':spot.time,
            'city':spot.city,
            'address':spot.address,
            'host':spot.host,
        }
        for spot in spot_list
    ]

    return JsonResponse(data, safe=False)