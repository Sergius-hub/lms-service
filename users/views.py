from rest_framework.request import Request
from rest_framework import viewsets

from users.models import Payment
from users.serializers import PaymentSerializer

# Платежи
class PaymentViewSet(viewsets.ModelViewSet):
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