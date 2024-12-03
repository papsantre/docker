from datetime import datetime, timedelta

import pytz
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from config import settings
from courses.models import Course, Lesson
from courses.paginators import CustomOffsetPagination, CustomPagination
from courses.serializers import (CourseCreateSerializer, CourseSerializer,
                                 LessonSerializer)
from courses.tasks import send_information_about_course_update
from users.permissions import IsModerator, IsOwner


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="Вывод списка курсов"),
)
@method_decorator(
    name="create", decorator=swagger_auto_schema(operation_description="Создание курса")
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление курса"),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(operation_description="Обновление курса"),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(operation_description="Обновление курса"),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(operation_description="Просмотр информации о курсе"),
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(reg_user=self.request.user)

    # serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CourseCreateSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

        # Никто. Никто не сможет подписаться на курс в момент его создания.

        # zone = pytz.timezone(settings.TIME_ZONE)
        # current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)
        #
        # course = get_object_or_404(Course, course.pk)
        #
        # if course.updated_at < current_datetime_4_hours_ago:
        #     send_information_about_course_update.delay(course.pk)
        #
        #
        # print(f"course.pk {course.pk}")
        # send_information_about_course_update.delay(course.pk)

    def perform_update(self, serializer):
        course = serializer.save()
        course.save()

        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)

        # course = get_object_or_404(Course, course.pk)

        if course.updated_at < current_datetime_4_hours_ago:
            send_information_about_course_update.delay(course.pk)

    def get_permissions(self):

        if self.request.user.groups.filter(name="Moderators").exists():

            if self.action in ["create", "destroy"]:
                self.permission_classes = (~IsModerator,)
            elif self.action in ["update", "retrieve"]:
                self.permission_classes = (IsModerator,)
        elif self.action != "create":
            self.permission_classes = (IsOwner,)
        return super().get_permissions()


class LessonListAPIView(ListAPIView):
    """Вывод списка уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomOffsetPagination


class LessonCreateAPIView(CreateAPIView):
    """Создание урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        new_lesson = serializer.save()

        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)

        course = get_object_or_404(Course, pk=new_lesson.course.pk)

        if new_lesson.course.updated_at < current_datetime_4_hours_ago:
            send_information_about_course_update.delay(course.pk)

        course.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    """Получение информации об отдельном уроке"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )


class LessonUpdateAPIView(UpdateAPIView):
    """Обновление информации об отдельном уроке"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )

    def perform_update(self, serializer):
        new_lesson = serializer.save()

        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)

        course = get_object_or_404(Course, pk=new_lesson.course.pk)

        if new_lesson.course.updated_at < current_datetime_4_hours_ago:
            send_information_about_course_update.delay(course.pk)

        course.save()


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    # почему-то удалять запрещает всем пользователям - какая-то особенность DRF?
    # permission_classes = (~IsModerator, IsAuthenticated)

    # а так - работает на модератора и дает удалять простому пользователю
    def get_permissions(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            self.permission_classes = (~IsModerator, IsAuthenticated)
        else:
            self.permission_classes = (IsOwner, IsAuthenticated)

        return super().get_permissions()
