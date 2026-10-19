from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from materials.paginators import MyPagination

# Курсы
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    #queryset = Course.objects.all()
    #permission_classes = [AllowAny,]
    def get_queryset(self):
        """Фильтруем queryset."""
        user = self.request.user
        qs = Course.objects.select_related("owner")

        if not user.is_authenticated:
            return qs.none()

        if user.is_staff or user.is_superuser or user.groups.filter(name="moderators").exists():
            return qs
        # return qs
        return qs.filter(owner=user)

    def get_permissions(self):

        if self.action == "list":
            self.permission_classes = (IsAuthenticated,)
        elif self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModerator)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, ~IsModerator | IsOwner)
        elif self.action in ("retrieve", "update", "partial_update"):
            self.permission_classes = (IsAuthenticated, IsModerator | IsOwner)

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Уроки
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)
    pagination_class = MyPagination

    def get_queryset(self):
        """Фильтруем queryset."""
        user = self.request.user
        qs = Lesson.objects.select_related("owner")

        if not user.is_authenticated:
            return qs.none()

        if user.is_staff or user.is_superuser or user.groups.filter(name="moderators").exists():
            return qs

        return qs.filter(owner=user)

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)

    def get_queryset(self):
        """Фильтруем queryset."""
        user = self.request.user
        qs = Lesson.objects.select_related("owner")

        if not user.is_authenticated:
            return qs.none()

        if user.is_staff or user.is_superuser or user.groups.filter(name="moderators").exists():
            return qs

        return qs.filter(owner=user)

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)

    def get_queryset(self):
        """Фильтруем queryset."""
        user = self.request.user
        qs = Lesson.objects.select_related("owner")

        if not user.is_authenticated:
            return qs.none()

        if user.is_staff or user.is_superuser or user.groups.filter(name="moderators").exists():
            return qs

        return qs.filter(owner=user)

class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner)

    def get_queryset(self):
        """Фильтруем queryset."""
        user = self.request.user
        qs = Lesson.objects.select_related("owner")

        if not user.is_authenticated:
            return qs.none()

        if user.is_staff or user.is_superuser or user.groups.filter(name="moderators").exists():
            return qs

        return qs.filter(owner=user)


class SubscriptionAPIView(APIView):
    """Установка/удаление подписки на курс."""

    permission_classes = [IsAuthenticated]

    def post(self, requset, *args, **kwargs):
        user = requset.user
        course_id = requset.data.get("course_id")
        if not course_id:
            return Response(
                {"error": "course_id обязателен."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена."
            is_subscribed = False
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена."
            is_subscribed = True

        return Response(
            {"message": message, "is_subscribed": is_subscribed},
            status=status.HTTP_200_OK,
        )

