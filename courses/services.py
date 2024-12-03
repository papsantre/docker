# from datetime import datetime, timedelta
#
# import pytz
# from django.shortcuts import get_object_or_404
#
# from config import settings
# from courses.models import Course
# from users.models import Subscriptions

#
# def get_email_list(pk):
#     """Отправляет сообщение пользователю об обновлении курса"""
#     subscriptions = Subscriptions.objects.filter(course=pk)
#
#     zone = pytz.timezone(settings.TIME_ZONE)
#     current_datetime_4_hours_ago = datetime.now(zone) - timedelta(minutes=4)
#
#     # print(pk)
#     course = get_object_or_404(Course, pk=pk)
#     # print(course)
#     # print(f"last_upd {course.updated_at}, -4h {current_datetime_4_hours_ago}")
#     #
#     # if course.updated_at < current_datetime_4_hours_ago:
#     #     print("updated is <")
#     # else:
#     #     print("updated is >")
#
#     email_list = []
#     message = f"Ваш курс {course.title} был обновлен!"
#     for s in subscriptions:
#         email_list.append(s.user.email)
#
#         print(f"email added = {s.user.email}")
#
#     return message, email_list
