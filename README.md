# Тестовое задание для компании GB
Проект выполнен для прохождения собеседования в консалтинговой компании
## О проекте
Проект выполняет функцию передачи показаний целевых датчиков в БД, для переобучения модели Machine Learning.
Проект разбит на несколько частей в порядке хронологического выполнения:
## Часть 0
Развернут Docker контейнера с БД Postgres.
Дополнительно к контейнеру БД был добавлен контейнер web на Django для облегчения дальнейшей разработки API.
## Этап 1
Написан скрипта для передачи показаний целевых датчиков в БД, развернутую в Docker.
Целевые датчики находятся в файле config.json и имеют вид:
```
{“loading_sensors”: [“sensor1”, “sensor5”, “sensor6”, “sensor8”, “sensor10” … “sensorN”]}
```
Скрипт периодический производит парсинг данных в .json файлах. Он выполнен в виде класса, а выполняется путем вызова
management command ```python manage.py jsonimport```

Сначала производится парсинг по дате, которая указана в названии файла и в его содержимом.
Между двумя данными значениями обнаружена разница (delta) порядка 1-2 секунд, с меньшим значением в содержимом файла.
Для ускорения работы скрипта парсинг производится по дате в названии файла. Для отладки написана функция delta_datetime.
В функцию парсинга передается нативная datetime, для применения проекта на проде нужно раскоментировать
некоторые блоки кода, где применяется datetime.now()

Далее показания целевых датчиков добавляются в коллекции, затем вычисляется их среднее значение за промежуток времени и
передается в БД качестве объектов Django ORM.
Файлы имеют вид:
```
sensors_2021-07-14_09_36_54.json
{
	“Timestamp”:”2021-07-14 09:36:54.038” # время снятия показаний
“sensor_values”:
[
	{“sensor_id”:”sensor1”, “value”:1.074},
	{“sensor_id”:”sensor2”, “value”:54.295},
	{“sensor_id”:”sensor3”, “value”:171.103},
	{“sensor_id”:”sensor5”, “value”:0.064},
	{“sensor_id”:”sensor12”, “value”:31.117},
	...
] 
}
```
Для проверки работы скрипта написаны тесты и данные для них.
## Этап 2
Для периодического выполнения скрипта был добавлен контейнер с celery, а также контейнер с redis для связи celery
и Django. Для связи Docker с папкой данных .json добавлен volume
## Этап 3
Начато написание API для одного эндпоинта:
```
POST: /api/write_values
```
## Шаблон наполнения env-файла, дополнительно указан в .env_example
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=qwerty
DB_HOST=db
DB_PORT=5432
SECRET_KEY = 'SECRET_KEY'
```
## Порядок запуска проекта
- Склонировать репозиторий и перейти в папку проекта через командную строку:
```
git@github.com/Flock1993/GB_test_task
```
```
cd /GB_testtask/
```
- Развернуть БД Postgres: при работающем приложении Docker выполнить команду:
```
docker-compose up
```
Создать суперюзера (ввести эмейл, пароль):
```
docker-compose exec web python manage.py createsuperuser
```
## Доступные возможности
Административный интерфейс
```
http://localhost:8000/admin/
```
Документация API, доступна только после входа в "админку"
```
http://localhost:8000/swagger/
```
Запуск тестов (пока написаны только для приложения json_import)
```
docker-compose exec web python manage.py test
```
Запуск management command для импорта показаний датчиков в базу данных
```
docker-compose exec web python manage.py jsonimport
```
## Для подключения БД Postgress, развернутую в контейнере, требуется указать следующие параметры
Host: ```localhost```
Port: ```5432```
User: ```POSTGRES_USER из .env```
Password: ```POSTGRES_PASSWORD из .env```
## Доступные эндпоинты
Запись показаний датчика в базу данных 
POST http://localhost:8000/api/write_values
```
{
  "timestamp": "2021-06-01T19:41:59.244Z",
  "sensor_values": [
    {
      "sensor_id": "string",
      "value": "Decimal(10, 3)"
    }
  ]
}
```
Ответы
```
Status code: 200 
Body: { “status”: “Success”, desc: “Дополнительная информация”}

Status code: 400
Body: {“status”: ”Error”, “desc”: “timestamp меньше чем максимальный timestamp в БД”}
```
## Дальнейшее развитие проекта
1. Отлавливать ошибку ```json.decoder.JSONDecodeError```
2. Автоматизировать создание тестовых данных для приложения json_import
3. Дописать API и автотесты
4. Добавить в скрипт импорта показаний датчиков, удаление файлов для ускорения поиска файлов
5. Производить поиск по файлам, отсортированным по названию, а следовательно и по дате.
Таким образом, достаточно найти первый и последний файл, попадающий во временной интервал
## Использованные технологии
Python 3.9, Django 3.2.15, Docker, Celery 5.2, Redis 4.3, Djangorestframework 3.12.4, Swagger
### Автор
Строков Матвей
