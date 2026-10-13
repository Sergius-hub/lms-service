from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework import generics
from django.http import Http404

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.permissions import IsSelfOrAdmin

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
        queryset = super().get_queryset()
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


# Пользователи
class BaseUserMixin():
    """Базовый класс миксин для CRUD пользователей."""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
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



