from django.contrib.auth.decorators import login_required
from join.models import Join_List
from homepage.models import NobarSpot
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from join.forms import JoinForm

def show_join(request):
    return render(request, "join.html")

@login_required(login_url='/account/login')
def post_join(request, nobar_place_id):
    form = JoinForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        nobar_place = get_object_or_404(NobarSpot, pk=nobar_place_id)
        existing_join = Join_List.objects.filter(user=request.user, nobar_place=nobar_place).first()

        # already joined?
        if existing_join:
            new_status = form.cleaned_data.get('status')

            # different status?
            if existing_join.status != new_status:
                existing_join.status = new_status
                existing_join.save(update_fields=['status'])
            return redirect('join:show_join')
        else:
            join_entry = form.save(commit=False)
            join_entry.user = request.user
            join_entry.nobar_place = nobar_place
            join_entry.save()
            return redirect('join:show_join')

    context = {'form': form}
    return render(request, "post_join.html", context)

def get_join(request):
    if (request.user.is_authenticated):
        join_list = Join_List.objects.filter(user=request.user)
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
