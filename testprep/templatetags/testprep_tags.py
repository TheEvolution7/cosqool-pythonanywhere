from testprep.models import Bookmark
from django import template
register = template.Library()


@register.inclusion_tag('bookmark.html', takes_context=True)
def bookmark(context, question):
    user = context.request.user
    object = context['object']
    bookmark = Bookmark.objects.filter(
        user=user, part=object, question=question, status=True).first()
    return {
        "object": bookmark,
        "part": object,
        "question": question
    }


@register.inclusion_tag('get_questions_by_part.html', takes_context=True)
def get_questions_by_part(context):
    object = context['object']
    user = context.request.user
    
    question_list = object.questions.filter().all()
    
    questions = []
    for question in question_list:
        obj = question 
        obj.bookmark = question.bookmark_questions.filter(user=user, part=object).first()
        questions.append(obj)
        
    return {
        "questions": questions
    }
