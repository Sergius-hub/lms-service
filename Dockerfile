# --- Этап 1: Сборщик (Builder) ---
# Используем официальный slim-образ Python 3.14
FROM python:3.14-slim AS builder

# Сначала меняем зеркало
RUN sed -i 's|deb.debian.org|mirror.yandex.ru|g' /etc/apt/sources.list.d/debian.sources

# Системные зависимости для сборки
RUN apt-get -o Acquire::ForceIPv4=true update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /build

# Copy dependens file to root dir
COPY requirements.txt .

# Собираем wheel-файлы
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# --- Этап 2: Финальный (Runtime) ---
FROM python:3.14-slim

# Сначала меняем зеркало
RUN sed -i 's|deb.debian.org|mirror.yandex.ru|g' /etc/apt/sources.list.d/debian.sources

# ВАЖНО: для psycopg в рантайме нужна библиотека libpq (не -dev!)
RUN apt-get -o Acquire::ForceIPv4=true update && apt-get install -y \
    libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY . .

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
