
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import datetime
from testpreps.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

class PartResultView(LoginRequiredMixin, generic.DetailView):
    model = TestprepResult


class PartResultDetailView(LoginRequiredMixin, generic.DetailView):
    model = PartResult

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        questions = Question.objects.filter(status=True, part=self.get_object().part).all()
        get_context_data.update({'questions': questions})
        return get_context_data
    
class TestPrepView(LoginRequiredMixin, generic.DetailView):
    model = TestPrep

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        testprep_results = self.get_object().testprep_results.filter(user=self.request.user).all().order_by(
            '-created_at')
        get_context_data.update({'testprep_results': testprep_results})
        return get_context_data

    def post(self, request, *args, **kwargs):
        testprep_result = TestprepResult.objects.create(
            user=request.user,
            testprep=self.get_object(),
        )
        
        self.request.session['testprep_result'] = str(testprep_result.pk)
        return HttpResponseRedirect(
            reverse("dashboards:testprep-part-questions",
                    kwargs={"pk": self.get_object().parts.first().pk})
        )


class TestPrepPartView(LoginRequiredMixin, generic.DetailView):
    model = Part

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        
        session_testprep_result = self.request.session['testprep_result']
        
        if session_testprep_result:
            part_result = PartResult.objects.filter(
                testprep_result=session_testprep_result,
                part=self.get_object(),
            ).first()
        
            if part_result is None:
                part_result = PartResult.objects.create(
                    testprep_result=TestprepResult.objects.filter(user=request.user).order_by("-created_at").first(),
                    part=self.get_object(),
            )

            return HttpResponseRedirect(
                reverse("dashboards:testprep-part-questions",
                        kwargs={"pk": self.get_object().pk})
            )
        return HttpResponseRedirect(
                reverse("dashboards:testprep-detail",
                        kwargs={"pk": self.get_object().testprep.pk})
            )
        
class TestPrepPartQuestionsView(LoginRequiredMixin, generic.DetailView):
    model = Part
    template_name = './testpreps/part_questions.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        session_testprep_result = self.request.session['testprep_result']
        
        has_clock = False
        expiration_time = datetime.datetime.now()
        
        next_url = {
            'text': f"View Result",
            'url': reverse("dashboards:testprep-detail", kwargs={"pk": self.get_object().testprep.pk})
        }
        
        if session_testprep_result is not None:
            part_result = PartResult.objects.filter(
                testprep_result=session_testprep_result,
                part=self.get_object(),
            ).first()
        
            
            if not part_result:
                part_result = PartResult.objects.create(
                    testprep_result_id=session_testprep_result,
                    part=self.get_object(),
                )
                has_clock = True
                expiration_time = part_result.created_at + datetime.timedelta(seconds=part_result.part.time.total_seconds())
            else:
                current_time = datetime.datetime.now(part_result.created_at.tzinfo)
                expiration_time = part_result.created_at + datetime.timedelta(seconds=part_result.part.time.total_seconds())
                if current_time < expiration_time:
                    has_clock = True
        
            try:
                next_url = {
                    'text': f"Next Part {self.get_object().get_next_in_order().get_order()}",
                    'url': reverse("dashboards:testprep-part-detail", kwargs={"pk": self.get_object().get_next_in_order().pk})
                }
            except ObjectDoesNotExist:
                next_url = {
                    'text': f"View Result",
                    'url': reverse("dashboards:testprep-result-detail", kwargs={"pk": part_result.testprep_result.pk})
                }
                
            
            try:
                previous = self.get_object().get_previous_in_order()
            except ObjectDoesNotExist:
                previous = 1
        
        context.update({
            'has_clock': has_clock, 
            'expiration_time': expiration_time,
            'next_url': next_url,
            'previous': previous
        })
        
        return context
    
    def post(self, request, *args, **kwargs):
        part_result = PartResult.objects.filter(
            testprep_result=self.request.session['testprep_result'],
            part=self.get_object(),
        ).first()
        save = True
        if part_result.content:
            save = False
            
        if part_result.status != "completed":
            current_time = datetime.datetime.now(part_result.created_at.tzinfo)
            expiration_time = part_result.created_at + datetime.timedelta(seconds=part_result.part.time.total_seconds())
            
            if current_time > expiration_time:
                save = False
                
        if save:
            data = request.POST
            data_ = dict(data.lists())
            data_.pop('csrfmiddlewaretoken')
            part_result.content = data_
            part_result.status='completed'
            part_result.save()
            
        try:
            return HttpResponseRedirect(
                reverse("dashboards:testprep-part-detail",
                        kwargs={"pk": self.get_object().get_next_in_order().pk})
            )
        except ObjectDoesNotExist:
            self.request.session['testprep_result'] = None
        
            return HttpResponseRedirect(    
                reverse("dashboards:testprep-result-detail",
                        kwargs={"pk": part_result.testprep_result.pk})
            )
        
        

class TestPrepResultView(LoginRequiredMixin, generic.DetailView):
    model = TestprepResult
    template_name = 'testpreps/testprep_result.html'