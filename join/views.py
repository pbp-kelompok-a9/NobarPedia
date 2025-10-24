from join.models import Join_List
from homepage.models import NobarSpot
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from join.forms import JoinForm

# done
def show_join(request):
    return render(request, "join.html")

# done just attach user and nobar_place into the request
def post_join(request, nobar_place_id):
    form = JoinForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        join_entry = form.save(commit = False)

        if request.user.is_authenticated:
            join_entry.user = request.user
        else:
            join_entry.user = None

        nobar_place = get_object_or_404(NobarSpot, id=nobar_place_id)
        join_entry.nobar_place = nobar_place

        join_entry.save()
        return redirect('join:show_join')

    context = {'form': form}
    return render(request, "post_join.html", context)

def get_join(request):
    join_list = Join_List.objects.all()
    data = [
        {
            'id': str(join_record.id),
            'user': join_record.user.username if join_record.user else None,
            'user_id': str(join_record.user.id) if join_record.user else None,
            'nobar_place_id': join_record.nobar_place_id,
            'nobar_place_name': join_record.nobar_place.name if join_record.nobar_place else None,
            'nobar_place_city': join_record.nobar_place.city if join_record.nobar_place else None,
            'nobar_place_time': join_record.nobar_place.time.strftime('%H:%M') if join_record.nobar_place and join_record.nobar_place.time
    else None,
            'status': join_record.status,
            'created_at': join_record.created_at.isoformat() if join_record.created_at else None,
        }
        for join_record in join_list
    ]

    return JsonResponse(data, safe=False)




def update_join(request, id):
    join_record = get_object_or_404(Join_List, pk=id)
    form = JoinForm(request.POST or None, instance=join_record)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('join:show_join')

    context = {
        'form': form
    }

    return render(request, "update_join.html", context)

def delete_join(request, id):
    join_record = get_object_or_404(Join_List, pk=id)
    join_record.delete()
    return HttpResponseRedirect(reverse('join:show_join'))
