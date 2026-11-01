from datetime import timedelta
from django.utils import timezone


from celery import shared_task
from users.models import User


@shared_task
def deactivate_inactive_users(minutes=10):
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