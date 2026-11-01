from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.permissions import IsSelfOrAdmin
from users.services import create_stripe_price, create_stripe_session


# Платежи
class PaymentViewSet(viewsets.ModelViewSet):
    """CRUD для payment."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Фильтрация, поиск, сортировка
    filterset_fields = [ "lesson", "method"]
    ordering_fields = ['paid_at']
    ordering = ["paid_at"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Payment.objects.none()

        queryset = super().get_queryset().filter(user=self.request.user)
        course = self.request.GET.get("course")
        lesson = self.request.GET.get("lesson")

        if course is None or lesson is None:
            return queryset
        # Фильтрация по Курсу
        if course == "null":
            queryset = queryset.filter(course__isnull=True)
        elif course and course.isdigit():
            queryset = queryset.filter(course_id=course)
        else:
            queryset = queryset.none()
        # Фильтрация по Уроку
        if lesson == "null":
            queryset = queryset.filter( lesson__isnull=True )
        elif lesson and lesson.isdigit():
            queryset = queryset.filter( lesson_id=lesson )
        else:
            queryset = queryset.none()

        return queryset

class CreateStripeSessionCheckoutAPIView(APIView):
    """Создание сессии stripe checkout."""
    permission_classes = [IsAuthenticated]

    def post(self, request):

        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                { "error": "course_id обязателен." },
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, pk=course_id)

        if not course.price:
            return Response(
                { "error": "У курса не установлена цена." },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Получаем Price в Stripe
        price = create_stripe_price( course.price, course.name )

        # 2. Checkout-сессия
        session_id, session_url = create_stripe_session(price)

        # 3. Создаем объект Payment (pending) в БД
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            method=Payment.Method.CARD,
            status=Payment.Status.PENDING,
            stripe_session_id=session_id,
            link=session_url,
        )

        return Response(
            { "payment_id": payment.id, "checkout_url": session_url },
            status=status.HTTP_201_CREATED,
        )

# Пользователи
class BaseUserMixin():
    """Базовый класс миксин для CRUD пользователей."""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        """Переопределяем query set для вывода только своих записей."""
        user = self.request.user
        qs = super().get_queryset()

        if not user.is_authenticated:
            return qs.none()

        # Админ видит всех
        if user.is_staff or user.is_superuser:
            return qs

        # Остальные — только себя
        return qs.filter(pk=user.pk)

    def get_object(self):
        """Переопределяем get_object для вывода своего сообщения."""
        try:
            return super().get_object()
        except Http404:
            raise Http404("Пользователь не найден.")

class UserCreateAPIView(BaseUserMixin, generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(is_active=True)

class UserListAPIView(BaseUserMixin, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

class UserRetrieveAPIView(BaseUserMixin, generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsSelfOrAdmin)

class UserUpdateAPIView(BaseUserMixin, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsSelfOrAdmin)

class UserDestroyAPIView(BaseUserMixin, generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsSelfOrAdmin)



