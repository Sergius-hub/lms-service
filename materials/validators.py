import re
from rest_framework import serializers


class YouTubeURLValidator:
    """Проверяет, что ссылка — на YouTube."""

    regex = re.compile(
        r"^https?://(?:(?:www|m)\.)?(?:youtube\.com|youtu\.be)/"
        r"(?:watch\?v=|embed/|v/|shorts/)?"
        r"(?P<video_id>[\w-]{11})(?:[&?].*)?$",
        re.IGNORECASE,
    )
    message = "Введите корректную ссылку на YouTube."
    code = "invalid_youtube"

    def __call__(self, value):
        if not value:
            return value
        if not self.regex.match(value):
            raise serializers.ValidationError(self.message, code=self.code)
        return value