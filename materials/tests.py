from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from materials.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com")
        self.course = Course.objects.create(name="test", description="test")
        self.lesson = Lesson.objects.create(name="lesson1", description="lesson1", course=self.course, owner=self.user)
        self.lesson = Lesson.objects.create(name="lesson2", description="lesson2", course=self.course, owner=self.user)
        self.lesson = Lesson.objects.create(name="lesson3", description="lesson3", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson-get', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), str(self.lesson.name))

    def test_lesson_create(self):
        url = reverse('materials:lesson-create')
        data = {
            "name": "lesson1",
            "course": self.course.pk,
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 4)

    def test_lesson_update(self):
        url = reverse('materials:lesson-update', kwargs={'pk': self.lesson.pk})
        data = {
            "name": "updated_lesson",
        }

        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "updated_lesson")

    def test_lesson_delete(self):
        url = reverse('materials:lesson-delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_list(self):
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data,
            {
                'count': 3,
                'next': None,
                'previous': None,
                'results': [{
                    'id': 10,
                    'name': 'lesson3',
                    'preview': None,
                    'description': 'lesson3',
                    'course': 3,
                    'reference': '',
                    'owner': 3
                }, {
                    'id': 9,
                    'name': 'lesson2',
                    'preview': None,
                    'description': 'lesson2',
                    'course': 3,
                    'reference': '',
                    'owner': 3
                }, {
                    'id': 8,
                    'name': 'lesson1',
                    'preview': None,
                    'description': 'lesson1',
                    'course': 3,
                    'reference': '',
                    'owner': 3
                }] }
        )

