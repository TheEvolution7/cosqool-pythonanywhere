from django.core.paginator import Paginator
from django.views.generic import TemplateView, DetailView, ListView
from .models import *

from django.contrib.auth import authenticate, login
from django.apps import apps

from pages.models import *
from menus.models import *
from settings.models import *
from fields.models import *
from articles.models import *
from accounts.models import *


def _get_settings(context):
    context["settings"] = {}

    for item in Setting.objects.all():
        if hasattr(item, "value"):
            context["settings"][item.slug] = item.value
    return context


def _get_base_context_data(context):
    context.update(_get_settings(context))
    return context


def _get_field(context, slug=None, model=Page):
    if slug is None:
        return context

    page = model.objects.filter(translations__slug=slug).first()
    page_type = ContentType.objects.get_for_model(model)
    fields = Field.objects.filter(
        group__content_type__pk=page_type.id, group__object_id=page.id
    ).all()
    context["fields"] = dict()
    for field in fields:
        context["fields"].update({field.id: field})
    return context


class WelcomeView(TemplateView):
    template_name = "welcome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _get_base_context_data(context)
        context.update(_get_field(context, ""))
        return context


class HomeView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = Page.objects.get(pk=1)
        fields = Field.objects.filter(
            group__page__pk=object.pk, group__status=True, status=True
        ).all()
        context["fields"] = {}
        for field in fields:
            context["fields"].update({field.id: field})

        context["articles"] = Article.objects.filter(categories__pk=1, status=True).all()
        context["faqs"] = Article.objects.filter(categories__pk=2, status=True).all()

        context["title"] = object.title
        context["description"] = object.description
        context["image"] = object.image

        context["meta"] = {
            "title": f"{object.title} | Learn online courses | Cosqool",
            "description": object.description,
            "image": object.image.url,
            "use_title_tag": True,
            "keywords": "",
            "use_og": True,
        }
        return context


class BaseDetialView(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        fields = Field.objects.filter(
            group__page__pk=self.get_object().pk, group__status=True, status=True
        ).all()

        context["fields"] = {}
        for field in fields:
            context["fields"].update({field.id: field})

        context["meta"] = {
            "title": f"{self.get_object().title} | Learn online courses | Cosqool",
            "description": self.get_object().description,
            "image": self.get_object().image and self.get_object().image.url or None,
            "use_title_tag": True,
            "keywords": "",
            "use_og": True,
        }

        return context


class PageView(BaseDetialView):
    model = Page
    slug_field = "translations__slug"

    def get_template_names(self):
        return "pages/" + self.kwargs.get("slug") + ".html"


class ArticleDetailView(BaseDetialView):
    model = Article

class CategoryView(BaseDetialView):
    model = ArticleCategory
