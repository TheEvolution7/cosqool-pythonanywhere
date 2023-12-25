
from lessons.models import *
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.generic.detail import SingleObjectMixin
from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course, Subject
from django.views import generic
from django.core.paginator import Paginator

from parler.views import TranslatableSlugMixin, ViewUrlMixin

from dashboards.views.playlists import *


class CoursesView(ViewUrlMixin, LoginRequiredMixin, generic.TemplateView):
    view_url_name = 'dashboards:course-detail'

    template_name = 'pages/dashboards/courses.html'

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)

        subjects = Subject.objects.filter().all()
        get_context_data.update({'subjects': subjects})

        return get_context_data


from notes.models import *
from reporterror.models import *
from testprep.models import TestPrep as TestPreps, TestprepResult, PartResult

class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('content',)


class NoteUpdateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('content',)


class ReportErrorCreateForm(forms.ModelForm):
    class Meta:
        model = ReportError
        fields = ('content',)


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        subjects = Subject.objects.filter(
            # grades__translations__slug=self.kwargs['grade']
        ).all()
        get_context_data.update({'subjects': subjects})

        # count_lesson = Lesson.objects.annotate(Count("pk"), filter=Q(
        #     section__course__translations__slug=self.kwargs['slug']
        # )
        # ).first()

        # get_context_data.update({'count_lesson': count_lesson})
        summary_list = [
            {
                "name": Lesson._meta.verbose_name,
                "data": Lesson.objects.filter().count(),
                "icon": "dashboard/assets/images/icon-courses/1.svg",
            },
            {
                "name": Quiz._meta.verbose_name,
                "data": Quiz.objects.filter().count(),
                "icon": "dashboard/assets/images/icon-courses/2.svg",
            },
        ]

        get_context_data.update({'summary_list': summary_list})

        notes = Note.objects.filter(user=self.request.user).all()
        get_context_data.update({'notes': notes})
        get_context_data.update({'note_create_from': NoteCreateForm})

        note_update_form_list = []
        for note in notes:
            form = NoteUpdateForm(instance=note)
            note_update_form_list.append(form)

        get_context_data.update({
            "note_update_form_list": note_update_form_list
        })

        get_context_data.update({'reporterror_form': ReportErrorCreateForm})
        get_context_data.update({'playlist_create_form': PlaylistCreateDashboardForm})

        return get_context_data



class CourseDetailVideoView(LoginRequiredMixin, generic.DetailView):
    model = Learn
    template_name = 'courses/course_detail_video.html'

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)

        subjects = Subject.objects.filter().all()
        get_context_data.update({'subjects': subjects})

        summary_list = [
            {
                "name": Lesson._meta.verbose_name_plural,
                "data": Lesson.objects.filter(status=True).count(),
                "icon": "dashboard/assets/images/icon-courses/1.svg",
            },
            {
                "name": Quiz._meta.verbose_name_plural,
                "data": Quiz.objects.filter(status=True).count(),
                "icon": "dashboard/assets/images/icon-courses/2.svg",
            },
            {
                "name": TestPrep._meta.verbose_name_plural,
                "data": TestPrep.objects.filter(status=True).count(),
                "icon": "dashboard/assets/images/icon-courses/9.svg",
            },
            {
                "name": Question._meta.verbose_name_plural,
                "data": Question.objects.filter(status=True).count(),
                "icon": "dashboard/assets/images/icon-courses/8_1.svg",
            },
            {
                "name": "Videos",
                "data": Learn.objects.filter(status=True).exclude(media__exact='').count(),
                "icon": "dashboard/assets/images/icon-courses/6.svg",
            },
        ]

        get_context_data.update({'summary_list': summary_list})

        get_context_data.update({
            "next": self.get_queryset().filter(pk__gt=self.get_object().pk).order_by("pk").first(),
            "previous": self.get_queryset().filter(pk__lt=self.get_object().pk).order_by("-pk").first(),
        })

        notes = Note.objects.filter(user=self.request.user).all()
        get_context_data.update({'notes': notes})
        get_context_data.update({'note_create_from': NoteCreateForm})

        note_update_form_list = []
        for note in notes:
            form = NoteUpdateForm(instance=note)
            note_update_form_list.append(form)

        get_context_data.update({
            "note_update_form_list": note_update_form_list
        })

        get_context_data.update({'reporterror_form': ReportErrorCreateForm})
        get_context_data.update({'playlist_create_form': PlaylistCreateDashboardForm})

        return get_context_data


class VideoView(LoginRequiredMixin, generic.DetailView):
    model = Learn
    slug_field = "pk"
    template_name = 'courses/video.html'


class TestPrepView(LoginRequiredMixin, generic.DetailView):
    model = TestPreps

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

        # part_result = PartResult.objects.create(
        #     testprep_result=testprep_result,
        #     part=self.get_object().parts.first(),
        # )

        return HttpResponseRedirect(
            reverse("dashboards:testprep:testprep-part-questions",
                    kwargs={"pk": self.get_object().parts.first().pk})
        )


class PartResultView(LoginRequiredMixin, generic.DetailView):
    model = TestprepResult


class PartResultDetailView(LoginRequiredMixin, generic.DetailView):
    model = PartResult

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        questions = Question.objects.filter(status=True, part=self.get_object().part).all()
        get_context_data.update({'questions': questions})
        return get_context_data




from django.core import serializers
from rest_framework.views import APIView
from rest_framework import generics
from testprep.serializers import *
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics


class BookmarkCreateView(APIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    model = Bookmark

    def get(self, request, format=None):
        snippets = Bookmark.objects.all()
        serializer = BookmarkSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        params = request.data.dict()
        part = Part.objects.filter(pk=params['part']).first()
        user = request.user
        question = Question.objects.filter(pk=params['question']).first()

        bookmark = Bookmark.objects.filter(part=part, user=user, question=question).first()

        if bookmark:
            if bookmark.status == True:
                bookmark.status = False
            else:
                bookmark.status = True

            params.update({'part': part.pk, 'user': user.pk, 'question': question.pk, 'status': bookmark.status})
            serializer = BookmarkSerializer(bookmark, data=params)
        else:
            params.update({'part': part.pk, 'user': user.pk, 'question': question.pk})
            serializer = BookmarkSerializer(data=params)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from notes.models import *
from notes.serializer import *


class NoteAPIView(APIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    model = Note

    def post(self, request, *args, **kwargs):
        params = request.data
        user = request.user
        params.update(user=user.pk)

        serializer = NoteSerializer(data=params)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteUpdateAPIView(generics.UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    model = Note

    def put(self, request, pk, format=None):
        params = request.data
        object = self.get_object()
        user = request.user
        params.update(user=user.pk)
        params.update(learn=object.learn.pk)
        serializer = NoteSerializer(object, data=params)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDestroyAPIView(generics.DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    model = Note

    def delete(self, request, pk, format=None):
        object = self.get_object()
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TestPrepPartView(LoginRequiredMixin, generic.DetailView):
    model = Part

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        part_result = PartResult.objects.create(
            testprep_result=TestprepResult.objects.filter(user=request.user).order_by("-created_at").first(),
            part=self.get_object(),
        )

        return HttpResponseRedirect(
            reverse("dashboards:testprep:testprep-part-questions",
                    kwargs={"pk": self.get_object().pk})
        )
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden()
        #
        # questions = []
        # data = request.POST
        # data_ = dict(data.lists())
        #
        # data_.pop('csrfmiddlewaretoken')
        #
        # for k in data_.keys():
        #     question = Question.objects.get(pk=k)
        #     questions.append(question)
        #
        # score = 0
        #
        # for q in questions:
        #     a_selected = request.POST.get(str(q.pk))
        #
        #     if a_selected != "":
        #         question_answers = Answer.objects.filter(question=q)
        #
        #         for a in question_answers:
        #
        #             if str(a_selected) == str(a.pk):
        #                 if a.correct:
        #
        #                     score += 1
        #
        # testprep_result = TestprepResult.objects.filter(
        #     user=request.user, testprep=self.get_object().testprep).order_by("-pk").first()
        #
        # part_result = PartResult.objects.create(
        #     part=self.get_object(),
        #     testprep_result=testprep_result,
        #     total_score=score, content=data_
        # )
        #
        # next_object = self.get_queryset().filter(pk__gt=self.get_object().pk,
        #                                          questions__isnull=False).order_by('pk').first()
        #
        # if next_object is not None:
        #     return HttpResponseRedirect(
        #         reverse("dashboards:testprep:testprep-part-detail",
        #                 kwargs={"pk": next_object.pk})
        #     )

        # return HttpResponseRedirect(
        #     reverse("dashboards:testprep:testprep-result-detail",
        #             kwargs={"pk": testprep_result.pk})
        # )

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
class TestPrepPartQuestionsView(LoginRequiredMixin, generic.DetailView):
    model = Part
    template_name = './testprep/part_questions.html'

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        return get_context_data

    def post(self, request, *args, **kwargs):
        testprep_result = TestprepResult.objects.filter(user=request.user, testprep=self.get_object().testprep).first()
        part_result = PartResult.objects.create(
            testprep_result=testprep_result,
            part=self.get_object(),
        )

        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        part_result.content = data_
        part_result.save()

        try:
            return HttpResponseRedirect(
                reverse("dashboards:testprep:testprep-part-questions",
                        kwargs={"pk": self.get_object().get_next_in_order().pk})
            )
        except Exception as e:
            pass

        return HttpResponseRedirect(
            reverse("dashboards:testprep:testprep-result-detail",
                    kwargs={"pk": part_result.testprep_result.pk})
        )

class TestPrepResultView(LoginRequiredMixin, generic.DetailView):
    model = TestprepResult
    template_name = 'testprep/testprep_result.html'


