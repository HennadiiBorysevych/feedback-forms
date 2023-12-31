from typing import Any
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
# Create your views here.

from .forms import ReviewForm
from .models import Review


class ReviewView(FormView):
    form_class = ReviewForm
    template_name = 'review/review.html'
    success_url = '/thank-you'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # def get(self, req):
    #     form = ReviewForm()
    #     return render(req, 'review/review.html', {"form": form})

    # def post(self, req):
    #     form = ReviewForm(req.POST)

    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect('/thank-you')


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


class ThankYouView(TemplateView):
    template_name = 'review/thank_you.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = 'This works'
        return context


class ReviewListView(ListView):
    template_name = "review/review_list.html"
    model = Review
    context_object_name = "reviews"


class SingleReviewView(DetailView):
    template_name = "review/single_review.html"
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        favorite_id = request.session.get('favorite_review', None)

        if favorite_id is not None:
            context['is_favorite'] = favorite_id == str(loaded_review.id)
        else:
            context['is_favorite'] = False

        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     review_id = kwargs["id"]
    #     selected_review = Review.objects.get(pk=review_id)
    #     context["review"] = selected_review
    #     return context


class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST['review_id']
        request.session['favorite_review'] = review_id

        return HttpResponseRedirect('/reviews/' + review_id)
