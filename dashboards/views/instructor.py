from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from accounts.models import Teacher
from django import forms
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.http import Http404

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = './instructors/custom_clearable_file_input.html'
    
class ProfileForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'headline', 'biography', 'language', 'website', 'facebook_url', 'twitter_url', 'linkedin_url', 'youtube_url', 'avatar', )
        widgets = {
            "avatar": CustomClearableFileInput()
        }
class InstructorBaseView(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.pk == 1 or request.user.groups.filter(name='Teacher').exists()):
            return super().dispatch(request, *args, **kwargs)
        else:
            if request.user:
                return redirect('dashboards:index')
            return redirect('accounts:login')
       
class IndexTemplateView(InstructorBaseView, TemplateView):
    template_name = 'instructors/index.html'
    
class ProfileTemplateView(InstructorBaseView, TemplateView):
    template_name = './instructors/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'profile_form': ProfileForm(instance=self.request.user.teacher)})
        return context
    
from courses.models import Course    
class CourseListView(InstructorBaseView, ListView):
    model = Course
    template_name = 'instructors/course_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

from accounts.models import Student  
class StudentListView(InstructorBaseView, ListView):
    model = Student
    template_name = 'instructors/student_list.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(enrollment__teacher=self.request.user.teacher).distinct().all()

class StudentDetailView(InstructorBaseView, DetailView):
    model = Student
    template_name = 'instructors/student_detail.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(enrollment__teacher=self.request.user.teacher)
    
    def get_object(self, queryset=None):
        return super().get_queryset().first()


from accounts.models import Enrollment  
from courses.models import Grade

class EnrollmentListView(InstructorBaseView, ListView):
    model = Enrollment
    template_name = 'instructors/enrollment_list.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(teacher=self.request.user.teacher, course__teacher=self.request.user.teacher).all().order_by("-id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        grade_list = Grade.objects.filter(status=True).all()
        status_list = Enrollment.STATUS_CHOICES
        
        context.update({
            'grade_list': grade_list,
            'status_list': status_list
        })
        return context
    
class EnrollmentDetailView(InstructorBaseView, DetailView):
    model = Enrollment
    template_name = 'instructors/enrollment_detail.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(teacher=self.request.user.teacher).all().order_by("-id")

from notification.models import NotificationTeacher    
class NotificationListView(InstructorBaseView, ListView):
    model = NotificationTeacher
    template_name = 'instructors/notification_list.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(teacher=self.request.user.teacher).all().order_by("-id")
    
    
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('accounts:login')