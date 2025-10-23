from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.db.models import Model
from django.core import serializers
from django.forms import Form
from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404


def match_main(request: HttpRequest):
    return render(request, 'match_main.html')


class BasicMatchAPIView(View):

    model_class: type[Model] = None
    form_class: type[Form] = None
    opt: chr = None

    def get(self, request: HttpRequest, *args, **kwargs):
        """Handles GET requests (e.g., reading/listing data)"""
        match self.opt:
            case 'r':
                return self.read_object(request, args[0])
            case _:
                return HttpResponseNotAllowed('opt not r for POST request')

    @method_decorator(login_required)
    @method_decorator(permission_required('main.admin'))
    def post(self, request: HttpRequest, *args, **kwargs):
        """Handles POST requests (e.g., creating data)"""
        match self.opt:
            case 'c':
                return self.create_object(request)
            case 'd':
                return self.delete_object(request, args[0])
            case 'u':
                return self.update_object(request, args[0])
            case _:
                return HttpResponseNotAllowed("opt not c, u, d for POST request")

    def read_object(self, request: HttpRequest, id):
        obj = get_object_or_404(self.model_class, pk=id)
        data = serializers.serialize('json', obj)
        return JsonResponse(data, safe=False)

    def create_object(self, request: HttpRequest):
        form = self.form_class(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        return HttpResponse(status=400)

    def delete_object(self, request: HttpRequest, id):
        obj = get_object_or_404(self.model_class, pk=id)
        obj.delete()
        return HttpResponse(status=202)

    def update_object(self, request: HttpRequest, id):
        obj = get_object_or_404(self.model_class, pk=id)
        form = self.form_class(request.POST, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        return HttpResponse(status=400)
