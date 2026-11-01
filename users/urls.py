from django.urls import path
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from rest_framework.permissions import AllowAny
from users.views import (
    PaymentViewSet,
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    CreateStripeSessionCheckoutAPIView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('user/login/', TokenObtainPairView.as_view(), name='token'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # CRUD пользователей
    path('user/register/', UserCreateAPIView.as_view(), name='user-register'),
    path('user/list/', UserListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/get/', UserRetrieveAPIView.as_view(), name='user-get'),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='users-update'),
    path('user/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='users-delete'),

    # Stripe Checkout
    path('payment/checkout/', CreateStripeSessionCheckoutAPIView.as_view(), name='payment-checkout'),
] + router.urls