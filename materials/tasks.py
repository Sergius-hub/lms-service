from datetime import timedelta
from django.utils import timezone


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

@shared_task
def deactivate_inactive_users(minutes=1):
    """
    Деактивирует пользователей, у которых last_login старше N минут.
    Только те, кто уже входил (last_login is not None).
    """
    cutoff = timezone.now()  - timedelta(minutes=minutes)

    # Только те, кто входил и last_login < cutoff
    # активные и не админы
    qs = User.objects.filter(
        last_login__isnull=False,
        last_login__lt=cutoff,
        is_active=True,
        is_staff=False,
    )

    count = qs.count()
    if count == 0:
        print("No users to deactivate")
        return 0

    updated = qs.update(is_active=False)
    print("Deactivated %s users (last_login < %s)", updated, cutoff)
    return updated