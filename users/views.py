from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import Payments, Subscriptions, User
from users.permissions import IsUserOwner
from users.serializers import (LimitedUserSerializer, PaymentsSerializer,
                               SubscriptionsSerializer, UserSerializer)
from users.services import create_stripe_price, create_stripe_session


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Просмотр информации о пользователе, обновление информации пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOwner, IsAuthenticated)

    def get_serializer_class(self):
        if self.request.method == "GET" and self.get_object() != self.request.user:
            return LimitedUserSerializer
        return UserSerializer

    def update(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return Response(
                {"detail": "You do not have permission to edit this user."}, status=403
            )
        return super().update(request, *args, **kwargs)


class UserListAPIView(ListAPIView):
    """Вывод списка пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteAPIView(DestroyAPIView):
    """Удаление пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOwner,)


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


# payments


class PaymentsListAPIView(ListAPIView):
    """Список платежей пользователей"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    """
    Настроить фильтрацию для эндпоинта вывода списка платежей с возможностями:

    - менять порядок сортировки по дате оплаты,
    - фильтровать по курсу или уроку,
    - фильтровать по способу оплаты.
    """

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method_is_cash")
    ordering_fields = ("date_of_payment",)


class PaymentsRetrieveAPIView(RetrieveAPIView):
    """Информация об отдельном платеже пользователя"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsUpdateAPIView(UpdateAPIView):
    """Обновление информации об отдельном платеже пользователя"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentsDestroyAPIView(DestroyAPIView):
    """Удаление платежа пользователя"""

    queryset = Payments.objects.all()


class SubscriptionsCreateAPIView(CreateAPIView):
    """Создание подписки на курс"""

    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubscriptionsDestroyAPIView(DestroyAPIView):
    """Удаление подписки на курс"""

    queryset = Subscriptions.objects.all()


class PaymentsCreateAPIView(CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.payment_amount)
        session_id, payment_link = create_stripe_session(price)

        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
