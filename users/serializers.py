from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Payments, Subscriptions, User


class UserSerializer(ModelSerializer):
    payments = SerializerMethodField(
        read_only=True, help_text="Оплаченные уроки и курсы"
    )
    subscriptions = SerializerMethodField(
        read_only=True, help_text="Подписки на обновления"
    )

    def get_payments(self, obj):
        return [
            f"{p.date_of_payment}-({p.payment_amount}, наличные: {p.payment_method_is_cash}),"
            for p in Payments.objects.filter(user=obj).order_by("date_of_payment")
        ]

    def get_subscriptions(self, obj):
        return [
            f"{s.course}-(pk={s.course.pk}{bool(s.last_date < s.course.updated_at)*' Курс обновлен!'}),"
            for s in Subscriptions.objects.filter(user=obj).order_by("last_date")
        ]

    class Meta:
        model = User
        fields = "__all__"


class LimitedUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"

    def create(self, validated_data):
        if validated_data.get("course") and validated_data.get("lesson"):
            raise ValidationError(
                "You can choose 'course' or 'lesson', but not both at the same time"
            )
        elif (
            validated_data.get("course") is None
            and validated_data.get("lesson") is None
        ):
            raise ValidationError("You must choose 'course' or 'lesson'")

        payment_item = Payments.objects.create(**validated_data)
        return payment_item

    def update(self, instance, validated_data):
        if validated_data.get("course") and validated_data.get("lesson"):
            raise ValidationError(
                "You can choose 'course' or 'lesson', but not both at the same time"
            )
        elif (
            validated_data.get("course") is None
            and validated_data.get("lesson") is None
        ):
            raise ValidationError("You must choose 'course' or 'lesson'")

        payment_item = Payments.objects.create(**validated_data)
        return payment_item


class SubscriptionsSerializer(ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = "__all__"
