from django.shortcuts import render

# Create your views here.
def show_homepage(request):
    context={}
    return render(request, "homepage.html",context)