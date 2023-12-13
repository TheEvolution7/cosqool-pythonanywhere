from .base import *

# from testpreps.models import *
from lessons.models import *
from django.urls import reverse
from django.shortcuts import redirect
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course, Subject
from django.views import generic
from django.core.paginator import Paginator
from django.contrib import messages
from parler.views import TranslatableSlugMixin, ViewUrlMixin

from dashboards.views.playlists import *


from notes.models import *
from reporterror.models import *

from notes.models import *
from reporterror.models import *
from quizzes.models import Answer, Question


class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("content",)


class NoteUpdateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("content",)


class ReportErrorCreateForm(forms.ModelForm):
    class Meta:
        model = ReportError
        fields = ("content",)


from subscriptions.models import Subscription


class CoursesView(DashboardView, TemplateView):
    template_name = "pages/dashboards/courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # subscriptions = Subscription.objects.filter(user=self.request.user, paypal_data__isnull=False).values_list("id", flat=True)
        # print(subscriptions)
        subjects = Subject.objects.filter().all()
        courses = Course.objects.filter().all()
        context.update({"subjects": subjects, "courses": courses})

        return context


class ProgressDetialsView(LoginRequiredMixin, DetailView):
    model = Course
    slug_field = "translations__slug"
    template_name = "pages/dashboards/progress_detail.html"


def quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    questions = quiz.question_set.filter().all()
    paginator = Paginator(questions, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    next_page = False
    show_summary = False
    if request.method == "POST":
        selected_choice = quiz.question_set.filter(
            answer__pk=request.POST["answer"]
        ).first()
        if (
            hasattr(selected_choice, "answer_set")
            and selected_choice.answer_set.get(pk=request.POST["answer"]).correct
        ):
            next_page = True

    results = {
        "next_page": next_page,
    }

    if next_page == True and page_obj.number == paginator.num_pages:
        show_summary = True
        results.update({"show_summary": show_summary})

    return TemplateResponse(
        request,
        "quizzes/quiz_detail.html",
        {
            "object": quiz,
            "lesson_items": LessonItem.objects.filter().all(),
            "results": results,
            "page_obj": page_obj,
        },
    )


# class PracticeView(View):
#     def get(self, request, *args, **kwargs):
#         view = PracticeDetailView.as_view()
#         return view(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         view = TakePracticeAnswerFormView.as_view()
#         return view(request, *args, **kwargs)


def practice(request, practice_id):
    practice = get_object_or_404(Practice, pk=practice_id)

    questions = practice.questions.filter().all()
    paginator = Paginator(questions, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    next_page = False
    show_summary = False
    if request.method == "POST":
        selected_choice = practice.questions.filter(
            answer__pk=request.POST["answer"]
        ).first()
        if (
            hasattr(selected_choice, "answer_set")
            and selected_choice.answer_set.get(pk=request.POST["answer"]).correct
        ):
            next_page = True

    results = {
        "next_page": next_page,
    }

    if next_page == True and page_obj.number == paginator.num_pages:
        show_summary = True
        results.update({"show_summary": show_summary})

    return TemplateResponse(
        request,
        "lessons/practice_detail.html",
        {
            "object": practice,
            "lesson_items": LessonItem.objects.filter().all(),
            "results": results,
            "page_obj": page_obj,
        },
    )


# class PracticeResultsView(LoginRequiredMixin, DetailView):
#     model = Practice
#     slug_field = "translations__slug"
#     template_name = "lessons/practice_results.html"

#     def get_context_data(self, **kwargs):
#         get_context_data = super().get_context_data(**kwargs)
#         lesson_items = LessonItem.objects.filter().all()
#         get_context_data.update({"lesson_items": lesson_items})
#         return get_context_data


# class QuizResultsView(LoginRequiredMixin, DetailView):
#     model = Quiz
#     slug_field = "translations__slug"
#     template_name = "quizzes/quiz_results.html"

#     def get_context_data(self, **kwargs):
#         get_context_data = super().get_context_data(**kwargs)
#         lesson_items = LessonItem.objects.filter().all()
#         get_context_data.update({"lesson_items": lesson_items})
#         return get_context_data


class ResultsView(LoginRequiredMixin, DetailView):
    model = SectionItem
    template_name = "quizzes/results.html"


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)

        video_list = LearnItem.objects.filter(
            learn__lesson__section__course=self.get_object()
        )
        paginator = Paginator(video_list, 1)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        get_context_data.update({"page_obj": page_obj})

        get_context_data.update({"sections": self.get_object().sections})
        notes = Note.objects.filter(user=self.request.user).all()
        get_context_data.update({"notes": notes})
        get_context_data.update({"note_create_from": NoteCreateForm})

        note_update_form_list = []
        for note in notes:
            form = NoteUpdateForm(instance=note)
            note_update_form_list.append(form)

        get_context_data.update({"note_update_form_list": note_update_form_list})

        get_context_data.update({"reporterror_form": ReportErrorCreateForm})
        get_context_data.update({"playlist_create_form": PlaylistCreateDashboardForm})

        return get_context_data


class SectionListView(LoginRequiredMixin, generic.ListView):
    model = Section


class SectionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Section


class SectionItemListView(LoginRequiredMixin, generic.ListView):
    model = SectionItem


class SectionItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = SectionItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_list = LearnItem.objects.filter(learn__lesson=self.get_object().pk)

        paginator = Paginator(video_list, 1)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context.update({"page_obj": page_obj})
        return context


class LessonListView(LoginRequiredMixin, generic.ListView):
    model = Lesson


class LessonDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lesson

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_list = LearnItem.objects.filter(learn__lesson=self.get_object()).all()

        paginator = Paginator(video_list, 1)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context.update({"page_obj": page_obj})
        return context


class LearnListView(LoginRequiredMixin, generic.ListView):
    model = Learn


class LearnDetailView(LoginRequiredMixin, generic.DetailView):
    model = Learn


class LearnItemListView(LoginRequiredMixin, generic.ListView):
    model = LearnItem


class LearnItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = LearnItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.filter(quiz__pk=self.get_object().quiz_id)
        paginator = Paginator(questions, 25)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context.update({"page_obj": page_obj})
        return context


class VideoListView(LoginRequiredMixin, generic.ListView):
    model = Video


class VideoDetailView(LoginRequiredMixin, generic.DetailView):
    model = Video


class TestListView(LoginRequiredMixin, generic.ListView):
    model = Test

class TestDetailView(LoginRequiredMixin, generic.DetailView):
    model = Test

    def post(self, request, *args, **kwargs):

        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        sitting = Sitting.objects.create(
            current_score=0,
            test_id=self.get_object().pk,
            user_id=self.request.user.pk,
            user_answers = data_
        )

        return redirect("dashboards:test-detail", pk=self.get_object().pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sitting = Sitting.objects.filter(test=self.get_object().pk, user=self.request.user).first()
        context['sitting'] = sitting
        return context

from records.models import Sitting


class SittingListView(LoginRequiredMixin, generic.ListView):
    model = Sitting


class SittingDetailView(LoginRequiredMixin, generic.DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get("qid", None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return redirect("dashboards:test-detail", kwargs={"pk": self.get_object()})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = context["sitting"].get_questions(with_answers=True)
        return context


class CourseDetailVideoView(LoginRequiredMixin, generic.DetailView):
    model = Learn
    template_name = "courses/course_detail_video.html"

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)

        subjects = Subject.objects.filter().all()
        get_context_data.update({"subjects": subjects})

        get_context_data.update(
            {
                "next": self.get_queryset()
                .filter(pk__gt=self.get_object().pk)
                .order_by("pk")
                .first(),
                "previous": self.get_queryset()
                .filter(pk__lt=self.get_object().pk)
                .order_by("-pk")
                .first(),
            }
        )

        get_context_data.update(
            {"sections": self.get_object().lesson.section.course.sections}
        )

        notes = Note.objects.filter(user=self.request.user).all()
        get_context_data.update({"notes": notes})
        get_context_data.update({"note_create_from": NoteCreateForm})

        note_update_form_list = []
        for note in notes:
            form = NoteUpdateForm(instance=note)
            note_update_form_list.append(form)

        get_context_data.update({"note_update_form_list": note_update_form_list})

        get_context_data.update({"reporterror_form": ReportErrorCreateForm})
        get_context_data.update({"playlist_create_form": PlaylistCreateDashboardForm})

        return get_context_data


class VideoView(LoginRequiredMixin, generic.DetailView):
    model = Learn
    slug_field = "pk"
    template_name = "courses/video.html"


class LessonItemListView(LoginRequiredMixin, ListView):
    model = LessonItem


class LessonItemDetailView(LoginRequiredMixin, DetailView):
    model = LessonItem

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     paginator = Paginator(self.get_object().get_questions(), 1)
    #     page_number = self.request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)

    #     context.update({"page_obj": page_obj})
    #     return context

    # def post(self, request, **kwargs):
    #     course_id = self.get_object().lesson.section.course.pk
    #     lesson_item_id = self.get_object().pk

    #     # Assuming get_questions() returns the queryset you want to paginate
    #     paginator = Paginator(self.get_object().get_questions(), 1)
    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)

    #     # Check if there is a next page
    #     if page_obj.has_next():
    #         next_page_number = page_obj.next_page_number()
    #     else:
    #         url = reverse("dashboards:course-detail", kwargs={"pk": course_id})
    #         return HttpResponseRedirect(url)
    #         next_page_number = (
    #             paginator.num_pages
    #         )  # Redirect to the last page if there is no next page

    #     # Construct the URL for the next page
    #     url = reverse(
    #         "dashboards:lessonitem-detail",
    #         kwargs={"course_id": course_id, "pk": lesson_item_id},
    #     )
    #     url += f"?page={next_page_number}"

    #     return HttpResponseRedirect(url)
