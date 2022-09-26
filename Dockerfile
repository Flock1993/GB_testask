FROM python:3.9-slim

# Сделать директорию /app рабочей директорией.
WORKDIR /app

# Скопировать с локального компьютера файл зависимостей
# в директорию /app.
COPY requirements.txt /app

# Выполнить установку зависимостей внутри контейнера.
RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN python -m pip install --upgrade pip

# Скопировать содержимое директории /test_task c локального компьютера
# в директорию /app.
COPY test_task/ /app


# Выполнить запуск сервера разработки при старте контейнера.
CMD ["gunicorn", "test_task.wsgi:application", "--bind", "0:8000" ]