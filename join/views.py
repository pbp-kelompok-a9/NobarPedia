from django.shortcuts import render

# Create your views here.
def tes(request):
    context = {}
    return render(request, "tes.html", context)