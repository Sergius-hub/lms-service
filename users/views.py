from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


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
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(is_active=True)

