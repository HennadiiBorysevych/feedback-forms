from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
# Create your views here.

from .forms import ReviewForm
from .models import Review


class ReviewView(View):
    def get(self, req):
        form = ReviewForm()
        return render(req, 'review/review.html', {"form": form})

    def post(self, req):
        form = ReviewForm(req.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thank-you')


def review(req):
    if req.method == 'POST':
        existing_model = Review.objects.get(pk=1)
        form = ReviewForm(req.POST, instance=existing_model)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thank-you')
    else:
        form = ReviewForm()

    return render(req, 'review/review.html', {"form": form})


def thank_you(req):
    return render(req, 'review/thank_you.html')
