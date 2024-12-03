# Инструкции по запуску

1. На компьютере должен быть установлен Docker и docker-compose 
(инструкции по установке на сайте https://www.docker.com/)
2. Создание и последующий запуск контейнера командой **docker-compose up -d --build**

==============================================================================================
# дополнительная информация о проекте


# Entry points:

**Courses**:
http://localhost:8000/courses/

**Lessons**:

list: http://localhost:8000/courses/lessons/

retrieve: http://localhost:8000/courses/lessons/<int:pk>/

* update: http://localhost:8000/courses/lessons/<int:pk>/update/

create: http://localhost:8000/courses/lessons/create/

delete: http://localhost:8000/courses/lessons/<int:pk>/delete/

**users**

list: http://localhost:8000/users/

retrieve_update: http://localhost:8000/users/<int:pk>/retrieve_update/

**payments**

list: http://localhost:8000/payments/

retrieve: http://localhost:8000/payments/<int:pk>/

create: http://localhost:8000/payments/create/

update: http://localhost:8000/payments/<int:pk>/update/

delete: http://localhost:8000/payments/<int:pk>/delete/

# Загрузка данных

Фикстуры с данными в папке **data**, порядок загрузки

1) python3 manage.py loaddata data/courses.json
2) python3 manage.py loaddata data/users.json

celery -A config worker --beat --scheduler django --loglevel=info

#config urls

urlpatterns = [

    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls", namespace="courses")),
    path("", include("users.urls", namespace="users")),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

#users urls

urlpatterns = [

    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path("users/<int:pk>/retrieve_update/", UserRetrieveUpdateAPIView.as_view(), name="users_retrieve_update"),
    path("users/<int:pk>/delete/", UserDeleteAPIView.as_view(), name="users_delete"),
    path("users/", UserListAPIView.as_view(), name="users"),
    # payments
    path("payments/", PaymentsListAPIView.as_view(), name="payments"),
    path("payments/<int:pk>/", PaymentsRetrieveAPIView.as_view(), name="payments_retrieve"),
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments_create"),
    path("payments/<int:pk>/update/", PaymentsUpdateAPIView.as_view(), name="payments_update"),
    path("payments/<int:pk>/delete/", PaymentsDestroyAPIView.as_view(), name="payments_delete"),
    # subscriptions
    path("subscriptions/create/", SubscriptionsCreateAPIView.as_view(), name="subscriptions-create"),
    path("subscriptions/<int:pk>/delete/", SubscriptionsDestroyAPIView.as_view(), name="subscriptions-delete")

]

#courses urls

urlpatterns = [

    path("lessons/", LessonListAPIView.as_view(), name="lessons-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons-retrieve"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons-update"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons-create"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lessons-delete"),

]
urlpatterns += router.urls

=========================================================
Задачи
Опишите Dockerfile для запуска контейнера с проектом.
(+) Оберните в Docker Compose Django-проект с БД PostgreSQL.
(+) Допишите в docker-compose.yaml работу с Redis.
(+) Допишите в docker-compose.yaml работу с Celery.
(+) Для выполнения заданий используйте проект для онлайн-обучения, над которым вы работали в рамках домашних заданий на курсе DRF.

========================================================

Критерии выполнения заданий
Оформили Dockerfile.
 Оформили файл docker-compose.yaml. (+)
 Инструкции по запуску находятся в файле Readme. (+ ?)
 Результат выполнения всего задания залили в GitHub и сдали в виде ссылки на репозиторий. (+)