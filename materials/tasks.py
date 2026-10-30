from celery import shared_task
from django.core.mail import send_mail
from users.models import User
from config.settings import DEFAULT_FROM_EMAIL

@shared_task
def send_subscription_email(user_pk, course_name):
    user = User.objects.get(pk=user_pk)
    send_mail(
        subject="Подписка на курс",
        message=f"Вы подписаны на курс: {course_name}.",
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )