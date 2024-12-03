from django.urls import reverse
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from courses.models import Course, Lesson
from users.models import User

#
"""
Напишите тесты, которые будут проверять корректность работы CRUD уроков и функционал работы подписки на обновления курса.

В тестах используйте метод 
setUp
 для заполнения базы данных тестовыми данными. Обработайте возможные варианты взаимодействия с контроллерами пользователей с разными правами доступа. Для аутентификации пользователей используйте 
self.client.force_authenticate()
. Документацию к этому методу можно найти тут.
"""


class CoursesTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")

        self.course = Course.objects.create(
            title="Курс номер 1", description="Описание курса номер 1", owner=self.user
        )

        video = "https://www.youtube.com/watch?v=uC0jJGfDxtM&list=PLlb7e2G7aSpTFea2FYxp7mFfbZW-xavhL&index=1"

        self.lesson = Lesson.objects.create(
            title="Урок номер 1",
            course=self.course,
            description="описание",
            video_url=video,
            owner=self.user,
        )

        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        # dogs:dog-detail
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        url = reverse("courses:course-list")
        data = {"title": "Курс 2"}
        response = self.client.post(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        data = {"title": "Курс 1"}
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Курс 1")

    def test_course_delete(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("courses:course-list")
        response = self.client.get(url)

        data = response.json()
        # print(data)

        created_text = str(self.course.created_at)
        created = created_text[0:10] + "T" + created_text[11:26] + "Z"
        updated_text = str(self.course.updated_at)
        updated = updated_text[0:10] + "T" + updated_text[11:26] + "Z"
        # print(f"created {created}")
        # print(f"updated {updated}")

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "title": self.course.title,
                    "preview": None,
                    "description": self.course.description,
                    "owner": self.user.pk,
                    "count_lessons": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "title": self.lesson.title,
                            "description": self.lesson.description,
                            "preview": None,
                            "video_url": self.lesson.video_url,
                            "course": self.course.pk,
                            "owner": self.user.pk,
                        }
                    ],
                    "created_at": created,
                    "updated_at": updated,
                    "subscriptions": False,
                }
            ],
        }
        # print(f"created_at:{self.course.created_at} updated_at:{self.course.updated_at}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")

        self.course = Course.objects.create(
            title="Курс номер 1", description="Описание курса номер 1", owner=self.user
        )

        video = "https://www.youtube.com/watch?v=uC0jJGfDxtM&list=PLlb7e2G7aSpTFea2FYxp7mFfbZW-xavhL&index=1"

        self.lesson = Lesson.objects.create(
            title="Урок номер 1",
            course=self.course,
            description="описание",
            video_url=video,
            owner=self.user,
        )

        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("courses:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("courses:lessons-create")
        # course_id = self.course.pk
        # print(self.course.pk)

        data = {"title": "lesson 2", "course": self.course.pk}

        response = self.client.post(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("courses:lessons-update", args=(self.lesson.pk,))
        data = {"title": "Updated lesson"}
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Updated lesson")

    def test_lesson_delete(self):
        url = reverse("courses:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("courses:lessons-list")
        response = self.client.get(url)

        data = response.json()
        # print(f"data {data}")

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "video_url": self.lesson.video_url,
                    "course": self.lesson.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }

        # print(f"result {result}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
