from ..views.playlists import *
from testprep.models import *
from django.utils.safestring import mark_safe
from menus.models import *
from notification.models import *
from django import template

register = template.Library()
from django.urls import reverse
from quizzes.models import Question, Answer as Answers

@register.inclusion_tag('templatetags/notification.html', takes_context=True)
def notification(context):
    notification_list = Notification.objects.filter(status=True).all()[:10]
    notification__not_read_count = Notification.objects.filter(
        status=True).count()

    context.update({
        'notification_list': notification_list,
        'notification__not_read_count': notification__not_read_count
    })
    return context


@register.inclusion_tag('templatetags/sidebar.html', takes_context=True)
def sidebar(context):
    linklist = Menu.objects.get(
        translations__slug="sidebar-dashboard").items.filter(status=True).all()
    context.update({
        'linklist': linklist
    })
    return context


def get_result_by_user(context, part_id, question_id, answer_id):
    result = PartResult.objects.filter(
        testprep_result=str(context.request.resolver_match.kwargs['pk']),
        content__has_key=str(question_id)
    ).first()

    answer = result.content[str(question_id)][0]
    return answer


@register.simple_tag(takes_context=True)
def get_answer_results_by_user(context, part_id, question_id, answer_id):
    answer = get_result_by_user(context, part_id, question_id, answer_id)

    get_answer = Answer.objects.filter(id=str(answer_id)).first()
    data = ''
    if answer == answer_id and get_answer.correct:
        data = 'right-col'

    if answer != answer_id and get_answer.correct:
        data = 'right-col'

    if answer == answer_id and get_answer.correct == False:
        data = 'wrong-col'

    return data


@register.simple_tag(takes_context=True)
def get_icon_answer_results_by_user(context, part_id, question_id, answer_id):
    data = ''
    get_answer = Answer.objects.filter(id=str(answer_id)).first()
    if get_answer.correct:
        data = '<i class="fa fa-check me-2"></i>'
    else:
        data = '<i class="fa fa-times me-2"></i>'

    answer = get_result_by_user(context, part_id, question_id, answer_id)

    if answer == answer_id:
        data += '<i class="fa fa-user me-2"></i>'

    return mark_safe(data)


@register.simple_tag()
def get_score_percent(obj):
    data = 0
    data = (obj.get_total_score_part_result() / obj.get_total_score_part()) * 100
    return round(data)


class PlaylistUpdateForm(forms.Form):
    playlist = forms.ModelChoiceField(
        queryset=Playlist.objects, empty_label=None)

    def __init__(self, user, *args, **kwargs):
        super(PlaylistUpdateForm, self).__init__(*args, **kwargs)
        self.fields['playlist'].queryset = Playlist.objects.filter(user=user)


@register.inclusion_tag('update_playlist.html', takes_context=True)
def update_playlist(context):
    form = PlaylistUpdateForm(user=context.request.user)
    return {"form": form}


@register.inclusion_tag('get_partresult_by_prepresult.html', takes_context=True)
def get_partresult_by_testprepresult(context, id):
    parts = Part.objects.filter(testprep_id=id).all()
    return {
        "parts": parts
    }


@register.inclusion_tag('get_question_by_partresult.html', takes_context=True)
def get_question_by_partresult(context, id):
    questions = Question.objects.filter(part=id).all()

    return {
        "questions": questions
    }


@register.inclusion_tag('get_answer_by_question.html', takes_context=True)
def get_answer_by_question(context, id):
    answers = Answer.objects.filter(question=id).all()

    return {
        "answers": answers
    }


@register.inclusion_tag('get_partresult_by_part.html', takes_context=True)
def get_partresult_by_part(context, part_id):
    object = context['object']
    partresult = PartResult.objects.filter(part=part_id, testprep_result=object.pk).first()
    return {
        "partresult": partresult
    }


@register.inclusion_tag('get_answerresult.html', takes_context=True)
def get_answerresult(context, answer):
    question_id = answer.question.pk
    answer_result = PartResult.objects.filter(
        testprep_result=str(context.request.resolver_match.kwargs['pk']),
        content__has_key=str(question_id)
    ).first()

    get_answer = answer_result.content[str(question_id)][0]
    data = ''
    if str(answer.pk) == str(get_answer) and answer.correct:
        data = 'right-col'

    if str(answer.pk) != str(get_answer) and answer.correct:
        data = 'right-col'

    if str(answer.pk) == str(get_answer) and answer.correct == False:
        data = 'wrong-col'

    return {
        "data": data
    }


import json

from django.utils.dateparse import parse_duration
@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    days_str = f'{days} days ' if days else ''
    hours_str = f'{hours} hours ' if hours else ''
    minutes_str = f'{minutes} minutes ' if minutes else ''
    seconds_str = f'{seconds} seconds' if seconds and not hours_str else ''

    return f'{days_str}{hours_str}{minutes_str}{seconds_str}'

@register.filter
def duration_to_min(timedelta):
    total_minutes = int(timedelta.total_seconds() / 60)
    return f'{total_minutes} min'

@register.simple_tag(takes_context=True)
def get_result_answer(context, part_result_content, question, answer):
    if (part_result_content):
        if str(answer.pk) in part_result_content[str(question.pk)] and answer.correct:
            return 'right-col'

        if str(answer.pk) not in part_result_content[str(question.pk)] and answer.correct:
            return 'right-col'

        if str(answer.pk) in part_result_content[str(question.pk)] and answer.correct == False:
            return 'wrong-col'
    return None

@register.simple_tag(takes_context=True)
def get_result_question(context, part_result_content, question):
    # if part_result_content is not None and str(question.pk) in part_result_content:
    #     answer = Answers.objects.filter(status=True, question=question.pk, pk__in=part_result_content[str(question.pk)]).first()
    # if (part_result_content):
    #     if str(answer.pk) in part_result_content[str(question.pk)] and answer.correct:
    #         return 'right-answer'

    #     if str(answer.pk) not in part_result_content[str(question.pk)] and answer.correct:
    #         return 'right-answer'

    #     if str(answer.pk) in part_result_content[str(question.pk)] and answer.correct == False:
    #         return 'wrong-answer'
    return None


@register.simple_tag(takes_context=True)
def get_icon_result_answer(context, part_result_content, question, answer):
    data = ''
    if (answer.correct):
        data += '<i class="fa fa-check me-2"></i>'
    else:
        data = '<i class="fa fa-times me-2"></i>'

    if part_result_content and str(answer.pk) in part_result_content[str(question.pk)]:
        data += '<i class="fa fa-user me-2"></i>'

    return mark_safe(data)


@register.simple_tag(takes_context=True)
def get_total_correct_answer(context):
    object = context['object']
    total = 0
    for question in object.part.get_questions():
        for answer in question.answers.filter(status=True, correct=True).all():
            if object.content is not None and str(question.pk) in object.content and str(answer.pk) in object.content[str(question.pk)]:
                total += 1
    return total

@register.simple_tag(takes_context=True)
def get_percent(context):
    object = context['object']
    percent_total_correct = 0
    if get_total_correct_answer(context) > 0:
        percent_total_correct = get_total_correct_answer(context) / object.part.get_questions().count() * 100
    return format(percent_total_correct, '.2f')

@register.simple_tag(takes_context=True)
def get_total_answer_correct_by_part(context, part_id):
    object = context['object']
    part_result = PartResult.objects.filter(part=part_id, testprep_result=object.pk).first()

    total = 0
    if part_result:
        for question in part_result.part.get_questions():
            for answer in question.answers.filter(status=True, correct=True).all():
                if part_result.content is not None and str(question.pk) in part_result.content and str(answer.pk) in part_result.content[str(question.pk)]:
                    total += 1

    return total

@register.simple_tag(takes_context=True)
def get_percent_by_part(context, part_id):
    object = context['object']
    part_result = PartResult.objects.filter(part=part_id, testprep_result=object.pk).first()

    percent_total_correct = 0
    if get_total_answer_correct_by_part(context, part_id) > 0:
        percent_total_correct = get_total_answer_correct_by_part(context, part_id) / part_result.part.get_questions().count() * 100
    return format(percent_total_correct, '.2f')

@register.simple_tag(takes_context=True)
def get_total_question_by_testprep_result(context):
    object = context['object'].get_total_score_part()
    return object

@register.simple_tag(takes_context=True)
def get_total_answer_correct_by_testprep_result(context):
    object = context['object']
    part_results = object.get_part_results().filter().all()
    total = 0

    for part_result in part_results:
        for question in part_result.part.get_questions():
            for answer in question.answers.filter(status=True, correct=True).all():
                if part_result.content is not None and str(question.pk) in part_result.content and str(answer.pk) in part_result.content[str(question.pk)]:
                    total += 1

    return total

@register.simple_tag(takes_context=True)
def get_percent_answer_correct_by_testprep_result(context):

    percent_total_correct = 0
    if get_total_answer_correct_by_testprep_result(context) > 0:
        percent_total_correct = get_total_answer_correct_by_testprep_result(context) / get_total_question_by_testprep_result(context) * 100
    return format(percent_total_correct, '.2f')

from ..paypalAPI import *
import json

@register.inclusion_tag('show_subscription_details.html', takes_context=True)
def show_subscription_details(context, data):
    json_to_data = json.loads(data)
    subscription = showSubscriptionDetails(json_to_data['subscriptionID'])
    plan = showPlanDetails(subscription['plan_id'])
    
    return {'subscription':subscription, 'plan': plan, 'subscription_object': context['subscription']}

@register.inclusion_tag('get_list_transactions_for_subscription.html', takes_context=True)
def get_list_transactions_for_subscription(context, id):
    transactions = listTransactionsForSubscription(id, '2023-01-01T00:00:00.000Z')
    return transactions

from datetime import datetime
@register.filter
def formatted_time_paypal(time_string):
    parsed_time = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')
    formatted_time = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time

from lessons.models import LessonItem
@register.filter
def get_lessonitem_by_course(pk):
    lessonitem = LessonItem.objects.filter(lesson__section__course__pk=int(pk), status=True).first()
    url = reverse("dashboards:course-detail", kwargs={"pk": int(pk)})
    
    if lessonitem._meta.verbose_name == "Learn":
        url = reverse("dashboards:course-detail-video", kwargs={"course_id": int(pk), "pk": lessonitem.pk})
    # if lessonitem._meta.verbose_name == "Practice":
    #     url = reverse("dashboards:lessonitem-detail", kwargs={"course_id": int(pk), "pk": lessonitem.pk})
    return url

@register.inclusion_tag('get_first_item_by_lessonitem.html', takes_context=True)
def get_first_item_by_lessonitem(context, sectionitem):
    sectionitem = SectionItem.objects.get(pk=int(sectionitem.pk))
    
    url = reverse("dashboards:sectionitem-detail", kwargs={"pk":sectionitem.pk })
    
    icon = 'dashboard/assets/images/icon-courses/1.svg'
    type = None
    if hasattr(sectionitem, '_meta'):
        if sectionitem._meta.verbose_name == "Lesson":
            url = reverse("dashboards:lesson-detail", kwargs={"pk":sectionitem.pk })
            first = sectionitem.get_items().first()
            if first:
                type = first._meta.verbose_name
                if type == 'Learn':
                    icon = 'dashboard/assets/images/icon-menu-new/2.svg'
                    
                if type == 'Practice':
                    icon = 'dashboard/assets/images/icon-courses/2.svg'
    object = {
        'sectionitem': sectionitem,
        'icon': icon,
        'type': type,
        'url': url
    }
    
    return object