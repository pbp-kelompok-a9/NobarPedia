from join.models import Join_List, Nobar_Place
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from join.forms import JoinForm

def show_join(request):
    return render(request, "join.html")


def post_join(request):
    form = JoinForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        join_entry = form.save(commit = False)

        # join_entry.user = request.user
        join_entry.user = None

        # join_entry.nobar_place = request.nobar_place
        join_entry.nobar_place = None

        join_entry.save()
        return redirect('join:show_tes')

    context = {'form': form}
    return render(request, "post_join.html", context)

def get_join_list(request):
    join_list = Join_List.objects.all()
    data = [
        {
            'id': str(join_record.id),
            'user_id': join_record.user_id,
            'nobar_place_id': join_record.nobar_place_id,
            'status': join_record.status,
            'created_at': join_record.created_at.isoformat() if join_record.created_at else None,
        }
        for join_record in join_list
    ]

    return JsonResponse(data, safe=False)

def get_join_record(request, id):
    try:
        join_record = Join_List.objects.select_related('user').get(pk=id)
        data = {
            'id': str(join_record.id),
            'user_id': join_record.user_id,
            'nobar_place_id': join_record.nobar_place_id,
            'status': join_record.status,
            'created_at': join_record.created_at.isoformat() if join_record.created_at else None,
        }
        return JsonResponse(data)
    except Join_List.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def update_join(request, id):
    join_record = get_object_or_404(Join_List, pk=id)
    form = JoinForm(request.POST or None, instance=join_record)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('join:show_tes')

    context = {
        'form': form
    }

    return render(request, "update_join.html", context)

def delete_join(request, id):
    join_record = get_object_or_404(Join_List, pk=id)
    join_record.delete()
    return HttpResponseRedirect(reverse('join:show_tes'))