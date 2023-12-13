from django import template

register = template.Library()
from django.urls import reverse
from sections.models import Section
from lessons.models import Lesson, Learn, Video, Test
from courses.models import Subject

@register.inclusion_tag("course_summary.html", takes_context=True)
def course_summary(context, pk):
    summary_list = [
        {
            "name": Section._meta.verbose_name_plural,
            "data": Section.objects.filter(course=pk).count(),
            "url": reverse("dashboards:section-list"),
        },
        {
            "name": Lesson._meta.verbose_name_plural,
            "data": Lesson.objects.filter(section__course=pk).count(),
            "url": reverse("dashboards:lesson-list"),
        },
        # {
        #     "name": TestPrep._meta.verbose_name_plural,
        #     "data": TestPrep.objects.filter().count(),
        #     "icon": "dashboard/assets/images/icon-courses/9.svg",
        # },
        # {
        #     "name": Question._meta.verbose_name_plural,
        #     "data": Question.objects.filter().count(),
        #     "icon": "dashboard/assets/images/icon-courses/8_1.svg",
        # },
        {
            "name": Learn._meta.verbose_name_plural,
            "data": Learn.objects.filter(lesson__section__course=pk).count(),
            "url": reverse("dashboards:learn-list"),
        },
        {
            "name": Video._meta.verbose_name_plural,
            "data": Video.objects.filter(learn__lesson__section__course=pk).count(),
            "url": reverse("dashboards:video-list"),
        },
        {
            "name": Test._meta.verbose_name_plural,
            "data": Test.objects.filter(learn__lesson__section__course=pk).count(),
            "url": reverse("dashboards:test-list"),
        },
    ]

    subjects = Subject.objects.filter()
    return {
        "summary_list": summary_list,
        "subjects": subjects
    }
