from tabnanny import check
from django import template

from quizzes.models import Answer, Question
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag("correct_answer.html", takes_context=True)
def correct_answer_for_all(context, question):
    """
    processes the correct answer based on a given question object
    if the answer is incorrect, informs the user
    """
    answers = question.get_answers()
    incorrect_list = context.get("incorrect_questions", [])
    if question.id in incorrect_list:
        user_was_incorrect = True
    else:
        user_was_incorrect = False

    return {"previous": {"answers": answers}, "user_was_incorrect": user_was_incorrect}


@register.filter
def answer_choice_to_string(question, answer):
    return question.answer_choice_to_string(answer)


import json


@register.inclusion_tag("correct_answer.html", takes_context=True)
def check_answer(context, question, answer):
    sitting = context["sitting"]
    user_answers = sitting.user_answers
    get_answer_list = user_answers.get(str(question.pk))

    correct_answer = Answer.objects.filter(
        pk=answer.pk, question=question.pk, correct=True
    ).first()

    alert = ""
    icon = ""
    checked = ""
    if get_answer_list and str(answer.pk) in get_answer_list:
        checked = "checked"
        icon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 16 16"><path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/></svg>'
        if not correct_answer:
            alert = "danger"

    if correct_answer:
        alert = "success"

        if get_answer_list and str(correct_answer.pk) in get_answer_list:
            alert = "success"

    return {
        "alert": alert,
        "icon": icon,
        "checked": checked,
        "question": question,
        "answer": answer,
    }
