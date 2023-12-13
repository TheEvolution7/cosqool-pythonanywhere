from django.contrib import admin
from .models import *


@admin.register(Overview)
class OverviewAdmin(admin.ModelAdmin):
    change_list_template = 'admin/overview_change_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        extra_context['performances'] = [
            {
                'label': 'Total sales',
                'data': {
                    'formatter': '$',
                    'value': 100,
                    'delta': 10,
                },
            },
            {
                'label': 'Net sales',
                'data': {
                    'formatter': '$',
                    'value': 1.00,
                    'delta': 1.5,
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
            {
                'label': 'Average order value',
                'data': {
                    'formatter': '$',
                    'value': 0.00,
                    'delta': 0,
                }
            },
            {
                'label': 'Products sold',
                'data': {
                    'formatter': '',
                    'value': 0,
                    'delta': 0,
                }
            },
            {
                'label': 'Downloads',
                'data': {
                    'formatter': '',
                    'value': 0,
                    'delta': 0,
                }
            },
            {
                'label': 'Gross sales',
                'data': {
                    'formatter': '$',
                    'value': 1.00,
                    'delta': 0,
                }
            },
            {
                'label': 'Variations sold',
                'data': {
                    'formatter': '',
                    'value': 0,
                    'delta': 0,
                }
            },

        ]

        extra_context['charts'] = [
            {
                'title': 'Net sales',
                'slug': 'net-sales',
                'formatter': '$',
                'data': {
                    'categories': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                    'series': [
                        {
                            'name': 'Now',
                            'data': [12.00, 19.01, 3.12, 15.99, 12.10, 13.00]
                        },
                        {
                            'name': 'Previous year',
                            'data': [20, 20, 31, 51, 21, 31]
                        }
                    ]
                }
            },
            {
                'title': 'Orders',
                'slug': 'orders',
                'data': {
                    'categories': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                    'series': [
                        {
                            'name': 'Now',
                            'data': [0, 9, 13, 5, 2, 3]
                        },
                        {
                            'name': 'Previous year',
                            'data': [2, 10, 1, 11, 0, 31]
                        }
                    ]
                }
            }
        ]

        extra_context['leaderboards'] = [
            {
                'title': 'Top categories - Items sold',
                'labels': ['Category', 'Total'],
                'data': [
                    {
                        'title': 'Elephant 1802',
                        'total': '10'
                    },
                    {
                        'title': 'Elephant 1802',
                        'total': '20'
                    }
                ]
            },
            {
                'title': 'Top Products - Items sold',
                'labels': ['Product', 'Total price'],
                'data': [
                    {
                        'title': 'Elephant 1802',
                        'total': '$100.00'
                    },
                    {
                        'title': 'Elephant 1802',
                        'total': '$200.00'
                    }
                ]
            }
        ]
        return super().changelist_view(
            request, extra_context=extra_context,
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = 'admin/analytic_change_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

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

        extra_context['charts'] = [
            {
                'title': 'Net sales',
                'slug': 'net-sales',
                'formatter': '$',
                'data': {
                    'categories': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                    'series': [
                        {
                            'name': 'Now',
                            'data': [12.00, 19.01, 3.12, 15.99, 12.10, 13.00]
                        },
                        {
                            'name': 'Previous year',
                            'data': [20, 20, 31, 51, 21, 31]
                        }
                    ]
                }
            },
            {
                'title': 'Orders',
                'slug': 'orders',
                'data': {
                    'categories': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                    'series': [
                        {
                            'name': 'Now',
                            'data': [0, 9, 13, 5, 2, 3]
                        },
                        {
                            'name': 'Previous year',
                            'data': [2, 10, 1, 11, 0, 31]
                        }
                    ]
                }
            },
            {
                'title': 'Total Sales',
                'slug': 'total-sales',
                'data': {
                    'categories': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                    'series': [
                        {
                            'name': 'Now',
                            'data': [10, 9, 130, 5, 2, 3]
                        },
                        {
                            'name': 'Previous year',
                            'data': [12, 10, 1, 11, 1, 11]
                        }
                    ]
                }
            }
        ]

        extra_context['leaderboards'] = [
            {
                'title': 'Top categories - Items sold',
                'labels': ['Category', 'Total'],
                'data': [
                    {
                        'title': 'Elephant 1802',
                        'total': '10'
                    },
                    {
                        'title': 'Elephant 1802',
                        'total': '20'
                    }
                ]
            },
            {
                'title': 'Top Products - Items sold',
                'labels': ['Product', 'Total price'],
                'data': [
                    {
                        'title': 'Elephant 1802',
                        'total': '$100.00'
                    },
                    {
                        'title': 'Elephant 1802',
                        'total': '$200.00'
                    }
                ]
            }
        ]
        return super().changelist_view(
            request, extra_context=extra_context,
        )


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    pass


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    pass
