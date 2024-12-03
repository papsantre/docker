from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from courses.models import Course, Lesson
from courses.validators import VideoUrlValidator
from users.models import Subscriptions


class LessonSerializer(ModelSerializer):
    validators = [VideoUrlValidator(field="video_url")]

    # serializers.UniqueTogetherValidator(fields=['title', 'description'], queryset=Lesson.objects.all())

    class Meta:
        model = Lesson
        fields = "__all__"

    # def create(self, validated_data):
    #
    #     lesson_item = Lesson.objects.create(**validated_data)
    #
    #     # При изменении урока, входящего в курс курс помечается как обновленный
    #     # Т.е. при его сохранении ставится текущее время обновления автоматом
    #     course_id = lesson_item.course.pk
    #     if(course_id):
    #         course_item = Course.objects.get(pk=course_id)
    #         course_item.save()
    #
    #     return lesson_item


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField(
        read_only=True, help_text="Число уроков в курсе"
    )
    lessons = LessonSerializer(
        many=True, read_only=True, help_text="Уроки, входящие в курс"
    )

    subscriptions = SerializerMethodField(
        read_only=True, help_text="Подписка текущего пользователя на курс"
    )

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")

        course_item = Course.objects.create(**validated_data)

        lesson_for_create = []

        for ls in lessons:
            lesson_for_create.append(Lesson(**ls, coutse=course_item))

        Lesson.objects.bulk_create(lesson_for_create)
        return course_item

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_subscriptions(self, obj):
        user = self.context["request"].user
        return Subscriptions.objects.all().filter(user=user).filter(course=obj).exists()

        # return [
        #     f"{s.course}-(pk={s.course.pk}{bool(s.last_date < s.course.updated_at) * ' Курс обновлен!'}),"
        #     for s in Subscriptions.objects.all().filter(course=obj).filter(user=user).order_by("last_date")
        # ]

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "preview",
            "description",
            "owner",
            "count_lessons",
            "lessons",
            "created_at",
            "updated_at",
            "subscriptions",
        )


class CourseCreateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
