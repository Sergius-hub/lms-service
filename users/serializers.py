from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "user", "paid_at", "amount", "method")
        read_only_fields = ("id", "user")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar")
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Хэшируем пароль перед сохранением."""
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для обновления поля last_login при логине пользователя"""
    def validate(self, attrs):
        data = super().validate(attrs)

        # Обновляем last_login
        user = self.user
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return data