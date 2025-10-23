from review.models import NobarSpot, reviewers
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from review.forms import ReviewForm
# Create your views here.

def show_reviews(request, nobar_spot_input):
    review_list = reviewers.objects.filter(nobar_spot=nobar_spot_input)
    context = {
        'review_list':review_list
    }
    return render(request, "main_review.html", context)

def create_review(request):
    form = ReviewForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        review_comment = form.save(commit=False)
        review_comment.user = request.user
        form.save()
        return redirect('review:main_review')
    context = {'form':form}
    return render(request, 'create_review.html', context)

def edit_review(request, id):
    review = get_object_or_404(reviewers, pk=id)
    form = ReviewForm(request.post or None, instance = review)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('review:main_review')
    context = {
        'form':form
    }
    return render(request, "update_review.html", context)

def delete_review(request, id):
    review = get_object_or_404(reviewers, pk=id)
    review.delete()
    return HttpResponseRedirect(reverse('review:main_review'))