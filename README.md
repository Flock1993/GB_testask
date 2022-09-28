# Тестовое задание для компании GB
Постановка задачи: преобразовать данные, поступающие с датчиков в формате json в базу данных
## Часть 0
Развертывание Docker контейнера с БД Postgres
## Часть 1
Command для импорта показаний датчиков из json файла в Б
## Порядок запуска проекта
- Склонировать репозиторий и перейти в папку проекта через командную строку:
```
git@github.com/Flock1993/GB_test_task
```
```
cd /GB_test_task/
```
- Развернуть БД Postgres: при работающем приложении Docker выполнить команду:
```
docker-compose up
```
Подготовить проект для миграций (при необходимости выполнить с префиксом ```mintty/winpty```):
```
docker-compose exec web python manage.py makemigrations
```
Произвести миграции:
```
docker-compose exec web python manage.py migrate
```
Создать суперюзера (ввести эмейл, пароль):
```
docker-compose exec web python manage.py createsuperuser
```
## Использованные технологии
Python 3.9, Django 3.2.15, Docker
### Автор
Строков Матвей
