from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentsCreateAPIView, PaymentsDestroyAPIView,
                         PaymentsListAPIView, PaymentsRetrieveAPIView,
                         PaymentsUpdateAPIView, SubscriptionsCreateAPIView,
                         SubscriptionsDestroyAPIView, UserCreateAPIView,
                         UserDeleteAPIView, UserListAPIView,
                         UserRetrieveUpdateAPIView)

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "users/<int:pk>/retrieve_update/",
        UserRetrieveUpdateAPIView.as_view(),
        name="users_retrieve_update",
    ),
    path("users/<int:pk>/delete/", UserDeleteAPIView.as_view(), name="users_delete"),
    path("users/", UserListAPIView.as_view(), name="users"),
    # payments
    path("payments/", PaymentsListAPIView.as_view(), name="payments"),
    path(
        "payments/<int:pk>/",
        PaymentsRetrieveAPIView.as_view(),
        name="payments_retrieve",
    ),
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments_create"),
    path(
        "payments/<int:pk>/update/",
        PaymentsUpdateAPIView.as_view(),
        name="payments_update",
    ),
    path(
        "payments/<int:pk>/delete/",
        PaymentsDestroyAPIView.as_view(),
        name="payments_delete",
    ),
    # subscriptions
    path(
        "subscriptions/create/",
        SubscriptionsCreateAPIView.as_view(),
        name="subscriptions-create",
    ),
    path(
        "subscriptions/<int:pk>/delete/",
        SubscriptionsDestroyAPIView.as_view(),
        name="subscriptions-delete",
    ),
]
