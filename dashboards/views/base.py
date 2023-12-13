# from subscriptions.models import *
import json
from haystack.query import SearchQuerySet
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.http import QueryDict
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.views import View
from django.template.response import TemplateResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from parler.views import TranslatableSlugMixin, ViewUrlMixin
from django.db.models import Q
from typing import Any, Dict
from django.db import models
from ..forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import views

from django.views.generic import TemplateView, DetailView, CreateView, FormView, ListView, View
from django.views.generic.edit import FormView
from ..models import *

from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

from mysite.permissions import *
from sections.models import *
# from quizzes.models import *
from courses.models import *
from lessons.models import *

from django.core.paginator import Paginator
from django import forms
from django.views.generic import DetailView

from django.http import HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from ..paypalAPI import *

class DashboardView(LoginRequiredMixin, View):
    pass

# from plans.models import Plan
from subscriptions.models import Subscription
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboards/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update(
            {'subscriptions': Subscription.objects.filter(user=self.request.user).all()})
        
        context.update(
            {'user_change_form': UserChangeForm(instance=self.request.user)})
        context.update(
            {'password_change_form': PasswordChangeForm(user=self.request.user)})
        return context


# class TakePracticeAnswerForm(forms.Form):
#     pass

# class TakePracticeAnswerFormView(FormView):
#     template_name = "books/author_detail.html"
#     form_class = TakePracticeAnswerForm
#     model = TakePracticeAnswer

#     slug_field = 'translations__slug'

#     def post(self, request, *args, **kwargs):

#         return super().post(request, *args, **kwargs)

#     def get_success_url(self):
#         return reverse("dashboards:practice", kwargs={"slug": 'count-with-small-numbers'})

# class PracticeDetailView(LoginRequiredMixin, DetailView):
#     model = Practice
#     slug_field = 'translations__slug'

#     def get_context_data(self, **kwargs):
#         get_context_data = super().get_context_data(**kwargs)
#         lesson_items = LessonItem.objects.filter().all()
#         get_context_data.update({'lesson_items': lesson_items})

#         questions = self.object.questions.filter().all()
#         paginator = Paginator(questions, 1)
#         page_number = self.request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         get_context_data.update({'page_obj': page_obj})

#         return get_context_data


# class QuestionDetailView(LoginRequiredMixin, DetailView):
#     model = Question


class ProgressView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboards/progress.html'

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        subjects = Subject.objects.filter().all()
        get_context_data.update({'subjects': subjects})
        return get_context_data


class HistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboards/history.html'

def autocomplete(request):
    q = request.GET['q']
    sqs = SearchQuerySet().auto_query(q)
    print(sqs)
    suggestions = [result.text for result in sqs]

    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')

from plans.models import *
from django.db.models import Q
from testpreps.models import TestPrep
class CheckoutView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        request = self.request.GET
        
        list_filter = Q()
        
        if request['plan']:
            list_filter &= Q(plan__translations__title=request['plan'])
            plan = Plan.objects.filter(Q(translations__title=request['plan'])).first()
            context.update({'plan_id': plan.pk})
        
        if request['option']:
            list_filter &= Q(option__translations__title=request['option'])
            option = Option.objects.filter(Q(translations__title=request['option'])).first()
            context.update({'option_id': option.pk})
        
        if request.get('grade') is not None:
            list_filter &= Q(grades__translations__title=request['grade'])
            grade = Grade.objects.filter(Q(translations__title=request['grade'])).first()
            context.update({'grade_id': grade.pk})
        
        if request.get('testprep') is not None:
            list_filter &= Q(testpreps__translations__title=request['testprep'])
            testprep = TestPrep.objects.filter(Q(translations__title=request['testprep'])).first()
            context.update({'testprep_id': testprep.pk})
            
        planitem = PlanItem.objects.filter(list_filter).first()
        context.update({'planitem': planitem})
        
        if planitem:
            context.update({'plan_object': showPlanDetails(planitem.paypal_plan_id)})
        return context
    
    template_name = "pages/dashboards/checkout.html"
    

class getListTransactionsForSubscription(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboards/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('accounts:login')