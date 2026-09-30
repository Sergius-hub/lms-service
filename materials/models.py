from django.db import models

class Course(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name="Название курса",
    )

    preview = models.ImageField(
        upload_to="images/materials/preview/",
        blank=True,
        null=True,
        verbose_name="Картинка курса",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["-id"]

    def __str__(self):
        return f"Курс \"{self.name}\""

class Lesson(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name="Название урока",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание урока",
    )

    preview = models.ImageField(
        upload_to="images/materials/preview/",
        blank=True,
        null=True,
        verbose_name="Картинка урока",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
    )

    reference = models.URLField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="Ссылка"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["-id"]

    def __str__(self):
        return f"Урок \"{self.name}\""