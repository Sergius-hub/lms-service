from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


# Курсы
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    #queryset = Course.objects.all()

    def get_queryset(self):
        user = self.request.user
        qs = Course.objects.select_related("owner")

        if user.is_staff or user.is_superuser or user.groups.filter(name="moderators").exists():
            return qs

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
    queryset = Lesson.objects.all()

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModerator)

