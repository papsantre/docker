from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from courses.models import Course
from users.models import Subscriptions


@shared_task
def send_information_about_course_update(pk):
    """Отправляет сообщение пользователю об обновлении курса"""
    subscriptions = Subscriptions.objects.filter(course=pk)

    # На счет того, что нельзя использовать get_object_or_404 - важная информация. Не знал.
    course = Course.objects.get(pk=pk)

    message = f"Ваш курс {course.title} был обновлен!"
    # for s in subscriptions:
    #     email_list.append(s.user.email)

    # The values_list() method returns a QuerySet containing tuples: <QuerySet [(1,), (2,)]>
    # values_list() with a single field, use flat=True to return a QuerySet instead of 1-tuples: <QuerySet [1, 2]>
    email_list = subscriptions.values_list('user_email', flat=True)

    if email_list:
        print(email_list)
        send_mail(f"Обновление курса.", message, EMAIL_HOST_USER, email_list)
