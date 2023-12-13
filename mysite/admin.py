import ast
from django.template.response import TemplateResponse
from django.contrib import admin
from settings.models import *
from django.urls import path
# from haystack.views import SearchView

from django.shortcuts import render

from urllib.parse import urlparse
from django.urls import resolve
from django.http import Http404, HttpResponseRedirect
from settings.models import *

from accounts.models import User
from django.apps import apps
import calendar
import random

# class CustomAdminView(SearchView):
#     def create_response(self):

#         self_admin_site = dict(
#             self.load_all['admin_site'].each_context(self.request),
#         )
#         context = self.get_context()
#         context.update(self_admin_site)

#         return render(self.request, self.template, context)


def get_dashboard(id):
    context = {}
    return context


def get_badge_for_model(model, menu):
    count = model['model'].objects.filter().count()
    badge = {
        'count': count,
        'message': f"{menu.title} {model['object_name']}",
        'color': menu.color
    }
    badges = [badge]
    if model.get('badges'):
        badges = model['badges']
        badges.append(badge)

    model.update({'badges': badges})

from django.urls import path, include
class MyAdminSite(admin.AdminSite):

    site_title = 'CMS'
    site_header = 'CMS'
    index_title = 'CMS'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("api/", include("mysite.router.admin")),
            
            # path('search/', self.admin_view(CustomAdminView(None, {'admin_site': self}),
            #      cacheable=True), name='search'),
            path('rebuild/', self.admin_view(self.rebuild,
                 cacheable=True), name='rebuild'),
            path('update/', self.admin_view(self.update,
                 cacheable=True), name='update')
        ]

        return my_urls + urls
    
    
    def get_app_list(self, request):
        get_app_list = super().get_app_list(request)
        custom_app_list = []

        for app in get_app_list:
            for model in app['models']:
                pass
            get_app = apps.get_app_config(app['app_label'])
            if hasattr(get_app, 'icon'):
                app.update(
                    {'icon': get_app.icon})

            custom_app_list.append(app)


        return custom_app_list

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['dashboard-1'] = {
            'card_title': 'Sales Progress',
            'card_body': {
                'chart': {
                    'series': [
                        {
                            'name': "Net Profit",
                            'data': [35, 65, 75, 55, 45, 60, 55]
                        },
                        {
                            'name': "Revenue",
                            'data': [40, 70, 80, 60, 50, 65, 60]
                        },
                    ],
                    'categories': ["Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                    'formatter': "$"
                }
            }
        }

        extra_context['users'] = User.objects.filter().all()[:5]
        extra_context['authors'] = User.objects.filter().all()[:5]

        extra_context['performances'] = [
            {
                'label': 'Items sold',
                'data': {
                    'formatter': '',
                    'value': 0,
                    'delta': 0,
                }
            },
            {
                'label': 'Net sales',
                'data': {
                    'formatter': '$',
                    'value': -1.00,
                    'delta': -1.5,
                }
            },
            {
                'label': 'Orders',
                'data': {
                    'formatter': '',
                    'value': 0,
                    'delta': 0,
                }
            },
        ]

        months = [month_name for month_number, month_name in enumerate(
            calendar.month_name) if month_number != 0]

        extra_context['charts'] = [
            {
                'title': 'Net sales',
                'slug': 'net-sales',
                'formatter': '$',
                'data': {
                    'categories': months,
                    'series': [
                        {
                            'name': 'Now',
                            'data': [random.randint(0, 1000) for _ in range(12)],
                            'count': sum([random.randint(0, 1000) for _ in range(12)])
                        },
                        {
                            'name': 'Previous year',
                            'data': [random.randint(0, 1000) for _ in range(12)],
                            'count': sum([random.randint(0, 1000) for _ in range(12)])
                        }
                    ],
                    'division': sum([random.randint(0, 1000) for _ in range(12)])/sum([random.randint(0, 1000) for _ in range(12)]),
                }
            },
            {
                'title': 'Orders',
                'slug': 'orders',
                'data': {
                    'categories': months,
                    'series': [
                        {
                            'name': 'Now',
                            'data': [random.randint(0, 100) for _ in range(12)],
                            'count': sum([random.randint(0, 100) for _ in range(12)])
                        },
                        {
                            'name': 'Previous year',
                            'data': [random.randint(0, 100) for _ in range(12)],
                            'count': sum([random.randint(0, 100) for _ in range(12)]),
                        }
                    ],
                    'division': sum([random.randint(0, 1000) for _ in range(12)])/sum([random.randint(0, 1000) for _ in range(12)]),
                }
            },
            {
                'title': 'Total Sales',
                'slug': 'total-sales',
                'data': {
                    'categories': months,
                    'series': [
                        {
                            'name': 'Now',
                            'data': [random.randint(0, 100) for _ in range(12)],
                            'count': sum([random.randint(0, 100) for _ in range(12)])
                        },
                        {
                            'name': 'Previous year',
                            'data': [random.randint(0, 100) for _ in range(12)],
                            'count': sum([random.randint(0, 100) for _ in range(12)])
                        }
                    ],
                    'division': sum([random.randint(0, 1000) for _ in range(12)])/sum([random.randint(0, 1000) for _ in range(12)]),
                }
            }
        ]

        return super().index(request, extra_context=extra_context)

    def each_context(self, request):
        each_context = super().each_context(request)
        each_context['settings'] = {}

        # myapp = apps.get_app_config('settings')
        # models = [model for model in myapp.get_models() if model.__name__ not in (
        #     'Language', 'LanguageTranslation', 'System')]

        # for model in models:
        #     for item in model.objects.all():
        #         if hasattr(item, 'value'):
        #             each_context['settings'][item.name] = item.value
        return each_context

    

    def rebuild(self, request):
        from django.core import management
        from django.core.management.commands import loaddata

        management.call_command('rebuild_index', '--noinput')
        # management.call_command('loaddata', 'y', verbosity=0)
        # management.call_command(loaddata.Command(), 'y', verbosity=0)

        # print(management.call_command('rebuild_index', verbosity=0))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def update(self, request):
        from django.core import management
        management.call_command('update_index')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
