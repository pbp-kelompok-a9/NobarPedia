from django.shortcuts import render, redirect, get_object_or_404
from homepage.forms import NobarSpotForm
from homepage.models import NobarSpot
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from join.models import Join_List # Import Join_List
from match.forms import MatchForm

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

def show_json(request):
    spot_list = NobarSpot.objects.all()
    json_data = serializers.serialize("json", spot_list)
    return HttpResponse(json_data, content_type="application/json")

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
