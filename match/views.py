from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.db.models import Model
from django.forms.models import model_to_dict
from django.core import serializers
from django.forms import Form
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from . import models


def get_match_spots(request: HttpRequest, match_id):
    obj = models.Match.objects.get(pk=match_id).shownAt.all()
    data = serializers.serialize("json", obj)
    return JsonResponse(data, safe=False)


def match_main(request: HttpRequest):
    model_type = request.GET.get("model_type", "match")
    if model_type == "match":
        data = models.Match.objects.all()
    elif model_type == "competition":
        data = models.Competition.objects.all()
    else:
        data = models.Player.objects.all()

    return render(request, 'match_main.html', {
        'data': data,
        'model_type': model_type
    })


@method_decorator(csrf_exempt, name='dispatch')
class BasicMatchAPIView(View):

    model_class: type[Model] = None
    form_class: type[Form] = None
    opt: chr = None

    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, *args, **kwargs):
        """Handles GET requests (e.g., reading/listing data)"""
        match self.opt:
            case 'r':
                return self.read_object(request, kwargs['id'])
            case 'ra':
                return self.read_all(request)
            case 'ri':
                return self.get_img(request, kwargs['id'])
            case _:
                return HttpResponseNotAllowed('opt not r for POST request')

    @method_decorator(require_POST)
    @method_decorator(csrf_exempt)
    def post(self, request: HttpRequest, *args, **kwargs):
        """Handles POST requests (e.g., creating data)"""
        match self.opt:
            case 'c':
                return self.create_object(request)
            case 'd':
                return self.delete_object(request, kwargs['id'])
            case 'u':
                return self.update_object(request, kwargs['id'])
            case _:
                return HttpResponseNotAllowed("opt not c, u, d for POST request")

    def read_object(self, request: HttpRequest, id):
        obj = get_object_or_404(self.model_class, pk=id)
        #data = model_to_dict(obj, exclude=['logo'])
        #data['id'] = str(obj.id)
        obj = [obj]
        data = serializers.serialize("json", obj)
        return JsonResponse(data, safe=False)
    
    def delete_object(self, request: HttpRequest, id):
        obj = get_object_or_404(self.model_class, pk=id)
        obj.delete()
        return JsonResponse({"status": "success"}, status=202)


    def read_all(self, request: HttpRequest):
        obj = self.model_class.objects.all()
        data = serializers.serialize("json", obj)
        print(data)
        return JsonResponse(data, safe=False)

    def create_object(self, request: HttpRequest):
        if not request.POST and request.body:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}
        else:
            data = request.POST

        form = self.form_class(data, request.FILES or None)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"}, status=201)
        return JsonResponse(form.errors, status=400)

    def update_object(self, request: HttpRequest, id):
        obj = get_object_or_404(self.model_class, pk=id)
        if not request.POST and request.body:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}
        else:
            data = request.POST

        form = self.form_class(data, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"}, status=201)
        return JsonResponse(form.errors, status=400)
