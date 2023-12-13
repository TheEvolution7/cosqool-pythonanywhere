from django.urls import path, include
from frontend.views import *
from accounts.views import *

app_name = "frontend"

urlpatterns = [
    # path('', WelcomeView.as_view(), name="welcome"),
    path("", HomeView.as_view(), name="home"),
    path(
        "article-categories/<slug:slug>",
        CategoryView.as_view(),
        name="article-category",
    ),
    path("articles/<slug:slug>", ArticleDetailView.as_view(), name="article-detail"),
    path("<slug:slug>/", PageView.as_view(), name="page-detail"),
    # path('about-us/', AboutUsView.as_view(), name="about-us"),
    # path('courses/', CoursesView.as_view(), name="courses"),
    # path('plans-pricing/', PlansPricingView.as_view(), name="plans-pricing"),
    # path('become-a-tutor/', BecomeATutorView.as_view(), name="become-a-tutor"),
    # path('contact-us/', ContactUsView.as_view(), name="contact-us"),
]
