from rest_framework import serializers
from materials.models import Course, Lesson
from materials.validators import YouTubeURLValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "name", "preview", "description", "course", "reference", "owner")
        read_only_fields = ("id", "owner")

        # Добавляем валидацию к полю
        extra_kwargs = {
            "reference": {
                "validators": [YouTubeURLValidator()],
            },
        }


class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ("id", "name", "preview", "description", "lesson_count", "lessons", "owner")
        read_only_fields = ("id", "lesson_count", "lessons", "owner")