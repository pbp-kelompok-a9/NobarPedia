from review.models import reviewers, NobarSpot
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from review.forms import ReviewForm
# Create your views here.

def show_test(request):
    return render(request, "tes.html")
    
def show_reviews(request, id):
    get_nobar_spot = get_object_or_404(NobarSpot, pk=id)
    review_list = reviewers.objects.filter(nobar_spot=get_nobar_spot)
    context = {
        'review_list':review_list,
    }
    return render(request, "show_reviews.html", context)

def create_review(request):
    form = ReviewForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        review_comment = form.save(commit=False)
        review_comment.user = request.user
        form.save()
        return redirect('review:show_reviews')
    context = {'form':form}
    return render(request, 'create_review.html', context)

def edit_review(request, id):
    review = get_object_or_404(reviewers, pk=id)
    form = ReviewForm(request.post or None, instance = review)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('review:show_reviews')
    context = {
        'form':form
    }
    return render(request, "update_review.html", context)

def delete_review(request, id):
    review = get_object_or_404(reviewers, pk=id)
    review.delete()
    return HttpResponseRedirect(reverse('review:main_review'))