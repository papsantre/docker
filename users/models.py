from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35, **NULLABLE, verbose_name="Телефон", help_text="Укажите телефон"
    )
    city = models.CharField(
        max_length=150,
        **NULLABLE,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.email}"


class Payments(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь внесший оплату",
        help_text="Введите пользователя, внесшего оплату",
        related_name="user",
        **NULLABLE,
    )

    date_of_payment = models.DateTimeField(
        auto_now_add=False,
        **NULLABLE,
        verbose_name="Дата оплаты",
        help_text="Укажите дату оплаты",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        **NULLABLE,
        related_name="course",
        verbose_name="Оплаченный курс",
        help_text="Введите оплаченный курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        **NULLABLE,
        related_name="lesson",
        verbose_name="Оплаченный урок",
        help_text="Введите оплаченный урок",
    )

    payment_amount = models.PositiveIntegerField(
        verbose_name="введите сумму оплаты", help_text="Введите сумму оплаты"
    )

    payment_method_is_cash = models.BooleanField(
        verbose_name="способ оплаты - наличные",
        help_text="Укажите признак оплаты наличными",
    )

    session_id = models.CharField(max_length=255, verbose_name="Id сессии", **NULLABLE)
    link = models.URLField(max_length=400, verbose_name="Cсылка на оплату", **NULLABLE)

    # CASH = 'cash'
    # NON_CASH = 'ncsh'
    #
    # PAYMENT_METHODS = (
    #     (None, 'Выберите тип оплаты'),
    #     (CASH, 'Наличные'),
    #     (NON_CASH, 'Безналичный рассчет')
    # )
    # payment_method = models.CharField(max_length=4, choices=PAYMENT_METHODS, **NULLABLE, verbose_name='способ оплаты',
    #                                   help_text='Укажите способ оплаты')

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"

    def __str__(self):
        return f"{self.user} ({self.course if self.course else self.lesson} - {self.payment_amount})"


"""
Добавьте модель подписки на обновления курса для пользователя.

Модель подписки должна содержать следующие поля: 

«пользователь» (FK на модель пользователя), «курс» (FK на модель курса). 

Можете дополнительно расширить модель при необходимости.
"""


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="подписчик",
        help_text="введите ID подписчика",
        related_name="subscriber",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="курс, на который создана подписка",
        help_text="введите ID курса подписки",
        related_name="subscribed_course",
    )
    last_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата начала подписки"
    )

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"

    def __str__(self):
        return f"{self.user} - {self.course}"
