from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from sections.models import *
from .models import *
from django.core.paginator import Paginator

class SectionItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = SectionItem
    slug_field = 'translations__slug'
    
    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        lesson_items = LessonItem.objects.filter().all()
        get_context_data.update({'lesson_items': lesson_items})
        
        if hasattr(self.object, 'question_set'):
            questions = self.object.question_set.filter().all()
            paginator = Paginator(questions, 1)
            page_number = self.request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            get_context_data.update({'page_obj': page_obj})
            
        return get_context_data

def get_next_or_prev(models, item, direction):
    getit = False
    if direction == 'prev':
        models = models
    for m in models:
        if getit:
            return m
        if item == m:
            getit = True
    if getit:
        return models[0]
    return False

class LearnDetailView(LoginRequiredMixin, generic.DetailView):
    model = Learn
    slug_field = 'pk'
    
    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        lesson_items = LessonItem.objects.filter().all()
        get_context_data.update({'lesson_items': lesson_items})
        
        get_context_data.update({
            'prev_object': self.get_queryset().filter(pk__lt=self.get_object().pk).order_by('-pk').first(),
            'next_object': self.get_queryset().filter(pk__gt=self.get_object().pk).order_by('pk').first()
        })
        
        return get_context_data