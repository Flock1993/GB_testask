FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN python -m pip install --upgrade pip

COPY test_task/ /app

# CMD ["gunicorn", "test_task.wsgi:application", "--bind", "0.0.0.0:8000", "--reload"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
