from django.urls import path
from rest_framework.routers import SimpleRouter

from courses.apps import CoursesConfig
from courses.views import (CourseViewSet, LessonCreateAPIView,
                           LessonDestroyAPIView, LessonListAPIView,
                           LessonRetrieveAPIView, LessonUpdateAPIView)

router = SimpleRouter()
router.register("", CourseViewSet)


app_name = CoursesConfig.name

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons-retrieve"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons-update"
    ),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons-create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lessons-delete",
    ),
]

urlpatterns += router.urls
