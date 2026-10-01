from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError


from materials.models import Course, Lesson

class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User"""
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Создание обычного пользователя"""
        if not email:
            raise ValueError("Email обязателен")

        # Нормализация email (приведение к нижнему регистру)
        email = self.normalize_email(email).lower()

        # Создание пользователя
        user = self.model(email=email, **extra_fields)

        # Установка пароля с хэшированием
        user.set_password(password)

        # Сохранение в БД
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        return self.create_user(email=email, password=password, **extra_fields)

class User(AbstractUser):
    """ Кастомная модель пользователя """
    username = None

    avatar = models.ImageField(
        upload_to="images/users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="Номер телефона",
    )

    city = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Город",
    )

    # Использование кастомного менеджера
    objects = UserManager()

    # Авторизация через email
    USERNAME_FIELD = 'email'

    # Обязательное поле для регистрации админа (createsuperuser)
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]

    def __str__(self):
        return f"\"{self.email}\": {self.first_name}"


class Payment(models.Model):
    """Модель Платежи"""

    class Method(models.TextChoices):
        CARD = "card", "Банковская карта"
        ACCOUNT = "account", "Счет банка"
        CASH = "cash", "Наличные"

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Пользователь"
    )

    paid_at = models.DateTimeField(
        verbose_name="Дата платежа"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Курс",
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Урок"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Сумма"
    )

    method = models.CharField(
        max_length=20,
        choices=Method.choices,
        default=Method.CARD,
        verbose_name="Способ оплаты"
    )

    def __str__(self):
        user = self.user if self.user else "-"
        return f"Платеж от {self.paid_at}, на сумму: {self.amount}, от пользователя: {user}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-paid_at"]