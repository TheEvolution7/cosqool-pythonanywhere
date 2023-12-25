from venv import create
from dashboards.views import testpresp
from .serializers import BookmarkSerializer, Bookmark
from core.api.views import *


class BookmarkViewSet(CoreViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer


class AdminBookmarkViewSet(AdminCoreViewSet, BookmarkViewSet):
    pass


class DashboardBookmarkViewSet(DashboardCoreViewSet, BookmarkViewSet):
    @action(detail=False, methods=["post"])
    def ajax_bookmark(self, request, format=None):
        user = request.user
        part = request.data["part"]
        question = request.data["question"]
        bookmark, created = Bookmark.objects.get_or_create(
            user=user, part_id=part, question_id=question
        )
        if not created:
            bookmark.delete()
            return Response({})

        serializer = BookmarkSerializer(bookmark)

        return Response(serializer.data)


from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import datetime
from testpreps.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect

import json


class PartResultView(LoginRequiredMixin, generic.DetailView):
    model = TestprepResult


# class PartResultDetailView(LoginRequiredMixin, generic.DetailView):
#     model = PartResult

#     def get_context_data(self, **kwargs):
#         get_context_data = super().get_context_data(**kwargs)
#         questions = Question.objects.filter(
#             status=True, part=self.get_object().part
#         ).all()
#         get_context_data.update({"questions": questions})
#         return get_context_data


class TestPrepListView(LoginRequiredMixin, generic.ListView):
    model = TestPrep

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timeline_list"] = TestprepResult.objects.filter(
            created_by=self.request.user.student, updated_by=self.request.user.student
        )
        return context


class TestPrepDetailView(LoginRequiredMixin, generic.DetailView):
    model = TestPrep

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = (
            self.get_object().testprep_results.filter(user=self.request.user).first()
        )
        context["testprep_results"] = result
        context["timeline_list"] = result.testprepresult_sectionresults.filter()
        return context

    def post(self, request, *args, **kwargs):
        testprep_result = TestprepResult.objects.create(
            user=request.user,
            testprep=self.get_object(),
        )

        self.request.session["testprep_result"] = str(testprep_result.pk)
        return HttpResponseRedirect(
            reverse(
                "dashboards:testprep-part-questions",
                kwargs={"pk": self.get_object().parts.first().pk},
            )
        )


class SectionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Section

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.get_object(), "get_parts"):
            context["part_list"] = self.get_object().get_parts

        testprep_result = TestprepResult.objects.filter(
            created_by=self.request.user.student,
            updated_by=self.request.user.student,
            testprep=self.get_object().testprep,
        ).first()

        if not testprep_result:
            testprep_result = TestprepResult.objects.create(
                testprep=self.get_object().testprep
            )

        section_result = TestprepItemResult.objects.filter(
            created_by=self.request.user.student,
            testprep_result=testprep_result,
            testprep_item=self.get_object(),
        ).first()

        context["section_result"] = section_result

        if section_result:
            current_time = section_result.created_at
            duration_seconds = self.get_object().time.total_seconds()
            time_remaining = current_time + datetime.timedelta(seconds=duration_seconds)
            context["time_remaining"] = time_remaining
        return context

    def post(self, request, *args, **kwargs):
        testprep_result = TestprepResult.objects.filter(
            created_by=self.request.user.student
        ).first()

        if request.POST["action"] and request.POST["action"] == "resume":
            part_result = (
                PartResult.objects.filter(
                    created_by=request.user.student, part__section=self.get_object()
                )
                .order_by("-created_at")
                .first()
            )
            current_part = part_result.part
            pk = current_part.pk

            check_next = False
            if part_result.user_answers and part_result.question_random_list:
                if len(part_result.user_answers) == len(
                    part_result.question_random_list
                ):
                    check_next = True

            if check_next:
                part_next = (
                    Part.objects.filter(
                        position__gt=current_part.position, section=self.get_object()
                    )
                    .exclude(pk=current_part.pk)
                    .order_by("position")
                    .first()
                )

                if part_next:
                    pk = part_next.pk

            return redirect("dashboards:testpreps:part-detail", pk=pk)

        if request.POST["action"] and request.POST["action"] == "begin":
            if testprep_result:
                testprep_result.status="in-progress"
                testprep_result.save()
                section_result = SectionResult.objects.filter(
                    created_by=request.user.student,
                    updated_by=request.user.student,
                    testprep_result=testprep_result,
                    testprep_item=self.get_object(),
                )

                if not section_result:
                    SectionResult.objects.create(
                        created_by=request.user.student,
                        updated_by=request.user.student,
                        testprep_result=testprep_result,
                        testprep_item=self.get_object(),
                    )

            part_first = (
                Part.objects.filter(section=self.get_object())
                .order_by("position")
                .first()
            )
            return redirect("dashboards:testpreps:part-detail", pk=part_first.pk)

        return redirect(
            "dashboards:testpreps:testprep-item-detail", pk=self.get_object().pk
        )


class TestPrepPartView(LoginRequiredMixin, generic.DetailView):
    model = Part

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_questions"] = self.get_object().max_questions
        context["question_list"] = []

        part_result = PartResult.objects.filter(
            part=self.get_object().pk,
        ).first()

        qs = self.get_object().get_random_questions()
        question_random_list = list(qs.values_list("pk", flat=True))

        if part_result:
            if not part_result.question_random_list:
                part_result.question_random_list = question_random_list
                part_result.save()

            context["part_result"] = part_result
        else:
            section_result = SectionResult.objects.filter(
                created_by=self.request.user.pk, updated_by=self.request.user.pk
            ).first()
            part_result = PartResult.objects.create(
                part=self.get_object(),
                section_result=section_result,
                question_random_list=question_random_list,
            )

        current_time = part_result.section_result.created_at
        duration_seconds = self.get_object().section.time.total_seconds()
        time_remaining = current_time + datetime.timedelta(seconds=duration_seconds)
        context["time_remaining"] = time_remaining

        context["question_list"] = Question.objects.filter(
            pk__in=part_result.question_random_list
        )

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        data_ = dict(data.lists())
        data_.pop("csrfmiddlewaretoken")

        part_result = PartResult.objects.filter(
            created_by=request.user.student, part=self.get_object()
        ).first()

        part_result.updated_by = self.request.user.student
        part_result.user_answers = data_
        part_result.save()

        current_part = self.get_object()
        pk = self.get_object().pk

        check_next = False
        if part_result.user_answers and part_result.question_random_list:
            if len(part_result.user_answers) == len(part_result.question_random_list):
                check_next = True

        if check_next:
            part_next = (
                Part.objects.filter(
                    position__gt=current_part.position,
                    section=self.get_object().section,
                )
                .exclude(pk=current_part.pk)
                .order_by("position")
                .first()
            )

            if part_next:
                pk = part_next.pk
            else:
                section_result = SectionResult.objects.filter(
                    created_by=request.user.student,
                    testprep_item=self.get_object().section.pk,
                ).first()

                section_result.status = "completed"
                section_result.completed_at = datetime.datetime.now()
                section_result.save()
                return redirect("dashboards:testpreps:testprep-list")

        return redirect("dashboards:testpreps:part-detail", pk=pk)


from django.core import serializers


class TestPrepPartQuestionsView(LoginRequiredMixin, generic.DetailView):
    model = Part
    template_name = "./testpreps/part_questions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        session_testprep_result = self.request.session["testprep_result"]

        has_clock = False
        expiration_time = datetime.datetime.now()

        next_url = {
            "text": "View Result",
            "url": reverse(
                "dashboards:testprep-detail",
                kwargs={"pk": self.get_object().testprep.pk},
            ),
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
                expiration_time = part_result.created_at + datetime.timedelta(
                    seconds=part_result.part.time.total_seconds()
                )
            else:
                current_time = datetime.datetime.now(part_result.created_at.tzinfo)
                expiration_time = part_result.created_at + datetime.timedelta(
                    seconds=part_result.part.time.total_seconds()
                )
                if current_time < expiration_time:
                    has_clock = True

            if not part_result.random_questions:
                random_questions = self.get_object().get_random_questions()
                part_result.random_questions = random_questions
                part_result.save()

            try:
                next_url = {
                    "text": f"Next Part {self.get_object().get_next_in_order().get_order()}",
                    "url": reverse(
                        "dashboards:testprep-part-detail",
                        kwargs={"pk": self.get_object().get_next_in_order().pk},
                    ),
                }
            except ObjectDoesNotExist:
                next_url = {
                    "text": f"View Result",
                    "url": reverse(
                        "dashboards:testprep-result-detail",
                        kwargs={"pk": part_result.testprep_result.pk},
                    ),
                }

            try:
                previous = self.get_object().get_previous_in_order()
            except ObjectDoesNotExist:
                previous = 1

        context.update(
            {
                "random_questions": Question.objects.filter(
                    pk__in=part_result.random_questions
                ).all(),
                "part_result": part_result,
                "has_clock": has_clock,
                "expiration_time": expiration_time,
                "next_url": next_url,
                "previous": previous,
            }
        )

        return context

    def post(self, request, *args, **kwargs):
        part_result = PartResult.objects.filter(
            testprep_result=self.request.session["testprep_result"],
            part=self.get_object(),
        ).first()
        save = True
        if part_result.content:
            save = False

        if part_result.status != "completed":
            current_time = datetime.datetime.now(part_result.created_at.tzinfo)
            expiration_time = part_result.created_at + datetime.timedelta(
                seconds=part_result.part.time.total_seconds()
            )

            if current_time > expiration_time:
                save = False

        if save:
            data = request.POST
            data_ = dict(data.lists())
            data_.pop("csrfmiddlewaretoken")
            part_result.content = data_
            part_result.status = "completed"
            part_result.save()

        try:
            return HttpResponseRedirect(
                reverse(
                    "dashboards:testprep-part-detail",
                    kwargs={"pk": self.get_object().get_next_in_order().pk},
                )
            )
        except ObjectDoesNotExist:
            self.request.session["testprep_result"] = None

            return HttpResponseRedirect(
                reverse(
                    "dashboards:testprep-result-detail",
                    kwargs={"pk": part_result.testprep_result.pk},
                )
            )


class TestPrepResultDetailView(LoginRequiredMixin, generic.DetailView):
    model = TestprepResult


class SectionResultDetailView(LoginRequiredMixin, generic.DetailView):
    model = SectionResult


class BreakeResultDetailView(LoginRequiredMixin, generic.DetailView):
    model = BreakeResult


class BreakeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Breake

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        testprep_result = TestprepResult.objects.filter(
            created_by=self.request.user.student
        ).first()

        if not testprep_result:
            testprep_result = TestprepResult.objects.create(
                testprep=self.get_object().testprep, user=self.request.user
            )

        breake_result = BreakeResult.objects.filter(
            created_by=self.request.user.student, testprep_result=testprep_result
        ).first()

        context["breake_result"] = breake_result
        
        if breake_result:
            current_time = breake_result.created_at
            duration_seconds = self.get_object().time.total_seconds()
            time_remaining = current_time + datetime.timedelta(seconds=duration_seconds)
            context["time_remaining"] = time_remaining
        

        return context

    def post(self, request, *args, **kwargs):
        testprep_result = TestprepResult.objects.filter(
            created_by=self.request.user.student
        ).first()

        if request.POST["action"] and request.POST["action"] == "leave":
            breake_result = BreakeResult.objects.filter(
                created_by=request.user.student,
                updated_by=request.user.student,
                testprep_result=testprep_result,
                testprep_item=self.get_object(),
            ).first()
            print(breake_result)
            if breake_result:
                breake_result.status = "completed"
                breake_result.completed_at = datetime.datetime.now()
                breake_result.save()

            return redirect("dashboards:testpreps:testprep-list")

        if request.POST["action"] and request.POST["action"] == "begin":
            if testprep_result:
                breake_result = BreakeResult.objects.filter(
                    created_by=request.user.student,
                    updated_by=request.user.student,
                    testprep_result=testprep_result,
                    testprep_item=self.get_object(),
                )

                if not breake_result:
                    breake_result = BreakeResult.objects.create(
                        created_by=request.user.student,
                        updated_by=request.user.student,
                        testprep_result=testprep_result,
                        testprep_item=self.get_object(),
                    )
            return redirect(
                "dashboards:testpreps:breake-detail", pk=breake_result.testprep_item.pk
            )


class TestPrepItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = TestPrepItem
