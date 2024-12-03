# Используем базовый образ Python
FROM python:3.10

# Настраиваем переменные окружения для poetry
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Устанавливаем poetry
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Добавляем poetry в переменную окружения PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Устанавливаем рабочую директорию в контейнере
WORKDIR /lms

# Установка зависимостей
COPY poetry.lock pyproject.toml ./
RUN poetry install

# Копируем код приложения в контейнер
COPY . .

# Команда для запуска приложения при старте контейнера
#CMD ["python", "app.py"]
#
## Python и Poetry идеально сочетаются.
#FROM python:3.8 as builder
#WORKDIR /app
#RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
#COPY pyproject.toml poetry.lock ./
#RUN poetry install --no-dev # Установка без зависимостей для разработки
#
## Финальный этап для Python, без Poetry.
#FROM python:3.8-slim
#WORKDIR /app
#COPY --from=builder /app ./
#CMD ["python", "your_app.py"] # Укажите основной скрипт вашего приложения