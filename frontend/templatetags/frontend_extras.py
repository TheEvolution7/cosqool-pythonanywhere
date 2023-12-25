from articles.models import *
from django import template
from django.core.paginator import Paginator
from settings.models import *
from menus.models import *
from courses.models import *
from products.models import *
from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

register = template.Library()


class CustomSelect(forms.Select):
    template_name = 'products/forms/select.html'


class CustomRadioSelect(forms.RadioSelect):
    template_name = 'products/forms/radio.html'
    option_template_name = 'products/forms/radio_option.html'

    def __init__(self, attrs=None, choices=(), price_map=None):
        self.price_map = price_map
        super().__init__(attrs, choices)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected,
                                       index, subindex=subindex, attrs=attrs)
        if self.price_map and value in self.price_map:
            option['attrs']['dataprice'] = self.price_map[value]
        return option

from plans.models import Plan
@register.inclusion_tag('get_plan_list.html', takes_context=True)
def get_plan_list(context):
    context['plan_list'] = list()
    plans = Plan.objects.filter().all()
    context.update({'plans': plans})
    return context


@register.inclusion_tag('courses/course_list.html', takes_context=True)
def get_course_list(context):
    grades = Grade.objects.filter(status=True).all()
    half = len(grades) // 2
    half += 1
    context.update({'grade_list': {
        'right': grades[:half],
        'left': grades[half:]
    }})
    return context


@register.inclusion_tag('articles/last_articles.html', takes_context=True)
def get_last_article(context):
    articles = Article.objects.filter().all()
    context.update({'articles': articles})
    return context


def _get_categories(context):
    category_list = ArticleCategory.objects.filter(parent=None).first()
    print(category_list)
    context.update({'category_list': category_list})
    return context


def _get_last_articles(context):
    last_article_list = Article.objects.filter().all()
    context.update({'last_article_list': last_article_list})
    return context


@register.inclusion_tag('articles/sidebar.html', takes_context=True)
def sidebar(context):
    _get_categories(context)
    _get_last_articles(context)
    return context


@register.inclusion_tag('articles/paginator.html', takes_context=True)
def article_paginator(context):
    if context['object'].__class__.__name__ == "Category":
        articles = Article.objects.filter(
            categories__pk=context['object'].id).all()
    else:
        articles = Article.objects.filter().all()

    paginator = Paginator(articles, 25)
    page_number = context.request.resolver_match.kwargs.get('page')
    page_obj = paginator.get_page(page_number)
    context.update({'page_obj': page_obj})
    return context


@register.inclusion_tag('metadata.html', takes_context=True)
def metadata(context):
    title = General.objects.filter(translations__name='site_title').first().value
    tagline = General.objects.filter(
        translations__name='tagline').first().value
    description = SEO.objects.filter(
        translations__name='meta_description').first().value

    metadata_title = f"{title} - {tagline}"
    metadata_description = description

    if context.get('object'):
        metadata_title = f"{context['object']} - {title}"

        if context['object'].description != '':
            metadata_description = context['object'].description

    context.update({
        'metadata': {
            'title': metadata_title,
            'description': metadata_description,
        }
    })
    return context


def _get_linklists(context, slug=None):
    for linklist in Menu.objects.filter(translations__slug=slug).all():
        context.update({
            'links': linklist.items.filter().all()
        })
    return context


@register.inclusion_tag('header.html', takes_context=True)
def header(context, slug):
    _get_linklists(context, slug)
    return context


@register.inclusion_tag('footer.html', takes_context=True)
def footer(context, slug):
    _get_linklists(context, slug)
    return context

@register.filter(name="image_tag")
def image_tag(value):
    return 'image_tag'

@register.filter(name="image_url")
def image_url(value):
    return 'image_url'

@register.filter(name="img_tag")
def img_tag(value):
    return 'img_tag'

@register.filter(name="img_url")
def img_url(value):
    if value:
        return value.url
    return settings.MEDIA_URL + 'default.png'

@register.filter(name="user_img_url")
def user_img_url(value):
    if value:
        return value.url
    return settings.MEDIA_URL + 'blank.png'

@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural

from urllib.parse import quote
from django.utils.encoding import iri_to_uri, uri_to_iri

@register.filter
def get_absolute_url(obj):
    return uri_to_iri(obj)

# import cv2
import datetime

import os

def format_duration(seconds):
    video_time = datetime.timedelta(seconds=seconds)
    if video_time.total_seconds() >= 3600:  # Check if the duration has hours
        time_str = str(video_time)
    else:
        time_str = str(video_time)[2:]  # Remove the leading "0:"
    return time_str

from django.urls import reverse
from django.http import HttpRequest

import argparse
import ffmpeg
import sys
# import cv2

@register.filter(name="get_duration_video")
def get_duration_video(obj):
    
    # parser = argparse.ArgumentParser(description='Get video information')
    # parser.add_argument('in_filename', help='Input filename')
    # args = parser.parse_args()
    # try:
    #     probe = ffmpeg.probe("https://cosqool.up.railway.app" + uri_to_iri(obj.url))
    # except ffmpeg.Error as e:
    #     print(e.stderr, file=sys.stderr)
    #     sys.exit(1)

    # video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    # if video_stream is None:
    #     print('No video stream found', file=sys.stderr)
    #     sys.exit(1)

    # width = int(video_stream['width'])
    # height = int(video_stream['height'])
    # num_frames = int(video_stream['nb_frames'])
    # print('width: {}'.format(width))
    # print('height: {}'.format(height))
    # print('num_frames: {}'.format(num_frames))
    
    # request = HttpRequest()
    # request.META['HTTP_HOST'] = 'localhost:8000'
    
    # file_path = os.path.join(settings.MEDIA_ROOT, obj.name)
    # data = cv2.VideoCapture(file_path)
    # frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    # fps = data.get(cv2.CAP_PROP_FPS)
    
    # # calculate duration of the video
    # seconds = 0
    # if frames and fps:
    #     seconds = round(frames / fps)
    print(os.path.join(settings.BASE_DIR, "staticfiles"))
    return format_duration(0)


@register.filter(name="get_progress_by_subject")
def get_progress_by_subject(subject):
    total_score_lesson = 1
    total_score_lesson_by_user = 1
    # if subject.grades:
    #     for course in subject.courses():
    #         for section in course.sections():
    #             for item in section.items():
    #                 pass
    #                 # total_score_lesson += item.get_total_score_lesson()
    #                 # total_score_lesson_by_user += item.get_total_score_lesson_by_user()
            
    return round(total_score_lesson_by_user/total_score_lesson*100)