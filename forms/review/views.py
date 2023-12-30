from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.

from .forms import ReviewForm


def review(req):
    if req.method == 'POST':
        form = ReviewForm(req.POST)
        if form.is_valid():
            print(form.cleaned_data)

            return HttpResponseRedirect('/thank-you')
    else:
        form = ReviewForm()

    return render(req, 'review/review.html', {"form": form})


def thank_you(req):
    return render(req, 'review/thank_you.html')
