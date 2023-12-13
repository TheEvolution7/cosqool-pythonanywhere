from django.urls import path, include, re_path
from .views import *
from courses.views import *
from playlists.views import *
from subscriptions.views import *
from reporterror.views import *

app_name = "dashboards"

palylists_patterns = (
    [
        path("", DashboardPlaylistListView.as_view(), name="index"),
        path("<uuid:pk>", DashboardPlaylistDetailView.as_view(), name="detail"),
        path("<uuid:pk>/update/", DashboardPlaylistUpdateView.as_view(), name="update"),
        path("<uuid:pk>/delete/", DashboardPlaylistDeleteView.as_view(), name="delete"),
    ],
    "playlists",
)

teacher_patterns = (
    [
        path("", AccountTeacherView.as_view(), name="index"),
    ],
    "teacher",
)

urlpatterns = [
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path(
        "my-profile/",
        include(
            [
                path("", ProfileView.as_view(), name="profile"),
                path(
                    "getListTransactionsForSubscription",
                    ProfileView.as_view(),
                    name="getListTransactionsForSubscription",
                ),
            ]
        ),
    ),
    path("playlists/", include("content.urls")),
    path(
        "my-course/",
        include(
            [
                path("", CoursesView.as_view(), name="list"),
                path("<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
                path("sections/", SectionListView.as_view(), name="section-list"),
                path(
                    "sections/<int:pk>",
                    SectionDetailView.as_view(),
                    name="section-detail",
                ),
                path(
                    "sectionitems/",
                    SectionItemListView.as_view(),
                    name="sectionitem-list",
                ),
                path(
                    "sectionitems/<int:pk>",
                    SectionItemDetailView.as_view(),
                    name="sectionitem-detail",
                ),
                path("lessons/", LessonListView.as_view(), name="lesson-list"),
                path(
                    "lessons/<int:pk>", LessonDetailView.as_view(), name="lesson-detail"
                ),
                path(
                    "lessonitems/",
                    LessonItemListView.as_view(),
                    name="lessonitem-list",
                ),
                path(
                    "lessonitems/<int:pk>",
                    LessonItemDetailView.as_view(),
                    name="lessonitem-detail",
                ),
                path("learns/", LearnListView.as_view(), name="learn-list"),
                path("learns/<int:pk>", LearnDetailView.as_view(), name="learn-detail"),
                path("learnitems/", LearnItemListView.as_view(), name="learnitem-list"),
                path(
                    "learnitems/<int:pk>",
                    LearnItemDetailView.as_view(),
                    name="learnitem-detail",
                ),
                path("videos/", VideoListView.as_view(), name="video-list"),
                path("videos/<int:pk>", VideoDetailView.as_view(), name="video-detail"),
                path("tests/", TestListView.as_view(), name="test-list"),
                path("tests/<int:pk>", TestDetailView.as_view(), name="test-detail"),

                path("marking/", SittingListView.as_view(), name="sitting-list"),
                path("marking/<int:pk>", SittingDetailView.as_view(), name="sitting-detail"),

                path(
                    "reporterror/",
                    ReportErrorCreateAPIView.as_view(),
                    name="reporterror",
                ),
                path("note/", NoteAPIView.as_view(), name="note"),
                path("note/<uuid:pk>", NoteUpdateAPIView.as_view(), name="note-update"),
                path(
                    "note/<uuid:pk>/delete",
                    NoteDestroyAPIView.as_view(),
                    name="note-delete",
                ),
                path("videos/<int:pk>", VideoView.as_view(), name="video-detail"),
                path(
                    "practice/<int:course_id>/<int:pk>",
                    LessonItemDetailView.as_view(),
                    name="lessonitem-detail",
                ),
                path(
                    "video/<int:course_id>/<int:pk>",
                    CourseDetailVideoView.as_view(),
                    name="course-detail-video",
                ),
                path(
                    "testprep/<uuid:pk>", TestPrepView.as_view(), name="testprep-detail"
                ),
                path(
                    "testprep/part/<uuid:pk>",
                    TestPrepPartView.as_view(),
                    name="testprep-part-detail",
                ),
                path(
                    "testprep/part/<uuid:pk>/questions",
                    TestPrepPartQuestionsView.as_view(),
                    name="testprep-part-questions",
                ),
                path(
                    "testprep/result/<uuid:pk>",
                    TestPrepResultView.as_view(),
                    name="testprep-result-detail",
                ),
                path(
                    "testprep/result/part/<uuid:pk>",
                    PartResultDetailView.as_view(),
                    name="part-result-detail",
                ),
            ],
        ),
    ),
    path("my-playlist/", include(palylists_patterns)),
    path(
        "my-progress/",
        include(
            [
                path("", ProgressView.as_view(), name="progress"),
                re_path(
                    r"^(?P<slug>[\u0600-\u06FF\w-]+)/$",
                    ProgressDetialsView.as_view(),
                    name="process-detail",
                ),
            ]
        ),
    ),
    path("my-history/", HistoryView.as_view(), name="history"),
    path("my-calendar/", ScheduleView.as_view(), name="caledar"),
    path("checkout/", CheckoutView.as_view(), name="ckeckout"),
    path("search/", autocomplete, name="search"),
    path("", AccountView.as_view(), name="index"),
    path("teacher/", include(teacher_patterns)),
    path("logout/", logout_view, name="logout"),
]


from rest_framework.routers import DefaultRouter

from accounts.views import DashboardAvatarViewSet, DashboardStudentViewSet

router = DefaultRouter()

router.register(r"api/students", DashboardStudentViewSet)
router.register(r"api/avatars", DashboardAvatarViewSet)
router.register(r"api/bookmarks", DashboardBookmarkViewSet)
router.register(r"api/subscriptions", DashboardSubscriptionViewSet)
router.register(r"api/playlists", DashboardPlaylistViewSet)
router.register(r"api/report-errors", DashboardReportErrorViewSet)

urlpatterns += router.urls
