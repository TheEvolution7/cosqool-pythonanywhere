from ast import Break
from venv import create
from quizzes.models import Question, Answer
from ..models import (
    Bookmark,
    PartResult,
    Section,
    SectionResult,
    TestPrepItem,
    Part,
    BreakeResult,
    TestprepItemResult,
)
from django import template
import datetime
import pytz
from django.db.models import Sum, Count

register = template.Library()


@register.inclusion_tag("bookmark.html", takes_context=True)
def bookmark(context, question):
    user = context.request.user
    object = context["object"]
    bookmark = Bookmark.objects.filter(
        user=user, part=object, question=question, status=True
    ).first()
    return {"object": bookmark, "part": object, "question": question}


@register.inclusion_tag("get_questions_by_part.html", takes_context=True)
def get_questions_by_part(context):
    object = context["object"]
    user = context.request.user

    question_list = context["random_questions"]

    questions = []
    for question in question_list:
        obj = question
        obj.bookmark = question.bookmark_questions.filter(
            user=user, part=object
        ).first()
        questions.append(obj)

    return {"questions": questions}


@register.simple_tag()
def get_question_by_pk(pk):
    question = Question.objects.get(pk=pk)
    return question.content


@register.inclusion_tag("testprep_section.html")
def testprep_section(obj):
    section_results = obj.section_sectionresults.filter()
    return {"obj": obj, "section_results": section_results}


@register.inclusion_tag("get_sectionresult_by_section.html", takes_context=True)
def get_sectionresult_by_section(context, item):
    testprep_item_result = TestprepItemResult.objects.filter(
        created_by=context.request.user.student.pk, testprep_item=item.pk
    ).first()

    prev_testprepitem = (
        TestPrepItem.objects.filter(
            position=item.position - 1,
            testprep=item.testprep,
        ).exclude(pk=item.pk)
        # .order_by("position")
        .all()[:1]
    )

    show = False
    if item.position == 1 and not testprep_item_result:
        show = True

    if prev_testprepitem:
        prev_section_result = (
            TestprepItemResult.objects.filter(
                created_by=context.request.user.student.pk,
                testprep_item=prev_testprepitem[0].pk,
            )
            .order_by("created_at")
            .first()
        )

        if prev_section_result:
            if (
                prev_section_result.status == "completed"
                or prev_section_result.status == "cancelled"
            ):
                show = True

    total_min_section_complete = 0
    total_seconds_section_complete = 0
    total_questions_complete = 0

    precent = 0
    total_precent_questions_complete = 0
    total_precent_min_complete = 0

    if testprep_item_result:
        if testprep_item_result._meta.model_name == "sectionresult":
            part_result_list = PartResult.objects.filter(
                created_by=context.request.user.student,
                section_result=testprep_item_result,
            )

            total_questions = item.get_total_questions()
            for part_result in part_result_list:
                if part_result.user_answers:
                    total_questions_complete += len(part_result.user_answers)

            total_precent_questions_complete = (
                total_questions_complete / total_questions * 100
            )

        now = datetime.datetime.now(tz=pytz.UTC)
        time_limit_section = testprep_item_result.created_at + item.time
        total_min_section_complete = item.time.total_seconds() // 60
        if (
            now > time_limit_section
            and testprep_item_result.status != "completed"
            and testprep_item_result.status != "cancelled"
        ):
            testprep_item_result.status = "cancelled"
            testprep_item_result.completed_at = datetime.datetime.now(tz=pytz.UTC)
            testprep_item_result.save()

        if (
            testprep_item_result.created_at
            and testprep_item_result.status != "cancelled"
        ):
            if testprep_item_result.status == "in-process":
                completed_at = datetime.datetime.now(tz=pytz.UTC)
                created_at = testprep_item_result.created_at

            if (
                testprep_item_result.status == "completed"
                and testprep_item_result.completed_at
            ):
                completed_at = testprep_item_result.completed_at
                created_at = testprep_item_result.created_at

            total_seconds_section_complete = (completed_at - created_at).total_seconds()
            if total_seconds_section_complete > item.time.total_seconds():
                total_seconds_section_complete = item.time.total_seconds()
            total_precent_min_complete = (
                total_seconds_section_complete / total_min_section_complete * 100
            )

        precent = total_precent_questions_complete

    return {
        "item": item,
        "testprep_item_result": testprep_item_result,
        "show": show,
        "total_seconds_section_complete": int(total_seconds_section_complete//60),
        "total_min_section_complete": round(total_min_section_complete),
        "total_questions_complete": total_questions_complete,
        "precent": precent,
    }


@register.inclusion_tag("get_part_result_for_testprepitem.html", takes_context=True)
def get_part_result_for_testprepitem(context, part):
    part_result = PartResult.objects.filter(
        created_by=context.request.user.student.pk, part=part
    ).first()

    complete = False
    total = 0
    if part_result:
        if part_result.user_answers:
            total = len(part_result.user_answers)

        if part_result.user_answers and part_result.question_random_list:
            if len(part_result.user_answers) == len(part_result.question_random_list):
                complete = True

    return {
        "part": part,
        "part_result": part_result,
        "complete": complete,
        "total": total,
    }


@register.simple_tag(takes_context=True)
def check_show_link_testprepitem(context, item):
    show = False
    first = (
        TestPrepItem.objects.filter(testprep=item.testprep.pk)
        .order_by("-position")
        .first()
    )
    current = SectionResult.objects.filter(
        created_by=context.request.user.student.pk, testprepitem=item.pk
    ).first()

    if first.pk == item.pk:
        show = True

    if current:
        previous = (
            SectionResult.objects.filter(
                created_by=context.request.user.student.pk,
                testprepitem=item.pk,
                id__lt=current.id,
            )
            .order_by("-id")
            .first()
        )

        if previous:
            show = True

    return show


@register.inclusion_tag("get_answer_for_part_result.html", takes_context=True)
def get_answer_for_part_result(context, question, answer):
    part_result = context["part_result"]
    user_answers = part_result.user_answers
    get_answer_list = user_answers.get(str(question.pk))

    icon = ""
    checked = ""

    if get_answer_list and str(answer.pk) in get_answer_list:
        checked = "checked"
        # icon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 16 16"><path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/></svg>'

    return {
        # "icon": icon,
        "checked": checked,
        "question": question,
        "answer": answer,
    }


@register.filter
def to_letter(value):
    english_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    arabic_letters_mapping = {
        "A": "ا",
        "B": "ب",
        "C": "ت",
        "D": "ث",
        "E": "ج",
        "F": "ح",
        "G": "خ",
        "H": "د",
        "I": "ذ",
        "J": "ر",
        "K": "ز",
        "L": "س",
        "M": "ش",
        "N": "ص",
        "O": "ض",
        "P": "ط",
        "Q": "ظ",
        "R": "ع",
        "S": "غ",
        "T": "ف",
        "U": "ق",
        "V": "ك",
        "W": "ل",
        "X": "م",
        "Y": "ن",
        "Z": "ه",
    }

    arabic_letters = "".join(
        arabic_letters_mapping.get(letter, letter) for letter in english_letters
    )
    return arabic_letters[value % len(arabic_letters)]
