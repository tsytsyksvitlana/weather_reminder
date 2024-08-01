[![Python](https://img.shields.io/badge/-Python-%233776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0a0a0a)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-092E20?style=for-the-badge&logo=django&logoColor=white&labelColor=0a0a0a)](https://www.djangoproject.com/)
[![Django Rest Framework](https://img.shields.io/badge/-Django%20Rest%20Framework-%2300B96F?style=for-the-badge&logo=django&logoColor=white&labelColor=0a0a0a)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/-Celery-37814A?style=for-the-badge&logo=celery&logoColor=white&labelColor=0a0a0a)](https://docs.celeryproject.org/)
[![SimpleJWT](https://img.shields.io/badge/-SimpleJWT-092E20?style=for-the-badge&logo=jsonwebtokens&logoColor=white&labelColor=0a0a0a)](https://github.com/jazzband/djangorestframework-simplejwt)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-%23316192?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=0a0a0a)](https://www.postgresql.org/)
[![SQLite](https://img.shields.io/badge/-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white&labelColor=0a0a0a)](https://www.sqlite.org/)
[![Docker](https://img.shields.io/badge/-Docker-%232496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0a0a0a)](https://www.docker.com/)
[![pre-commit](https://img.shields.io/badge/-pre--commit-yellow?style=for-the-badge&logo=pre-commit&logoColor=white&labelColor=0a0a0a)](https://pre-commit.com/)
[![isort](https://img.shields.io/badge/isort-enabled-brightgreen?style=for-the-badge&logo=isort&logoColor=white&labelColor=0a0a0a)](https://pycqa.github.io/isort/)

# DjangoWeatherReminder
***
## Generic setup
### Create .env file and fill with required data

```
SECRET_KEY = <YOUR_SECRET_KEY>
EMAIL_HOST_USER = <YOUR_EMAIL_HOST_USER>
EMAIL_HOST_PASSWORD = <YOUR_EMAIL_HOST_PASSWORD>
REDIS_HOST=<YOUR_REDIS_HOST>
WEB_HOST=<YOUR_WEB_HOST>
WEB_PORT=<YOUR_WEB_PORT>
PG_USER=<YOUR_PG_USER>
PG_PASS=<YOUR_PG_PASS>
PG_NAME=<YOUR_PG_NAME>
PG_HOST = <YOUR_PG_HOST>
PG_PORT =<YOUR_PG_PORT>
WEATHER_API_KEY = <YOUR_WEATHERBIT_IO_API_KEY>
TELEGRAM_BOT_TOKEN = <YOUR_TELEGRAM_BOT_TOKEN>
ADMIN_TG_CHAT_ID = <YOUR_ADMIN_TG_CHAT_ID>
TEST_PG_NAME = <YOUR_TEST_PG_NAME>
TEST_PG_USER = <YOUR_TEST_PG_USER>
TEST_PG_PASS = <YOUR_TEST_PG_PASS>
```
### Create home network
```
docker network create home
```
### Run docker-compose file
```
docker-compose up
```
### To see your application, visit
http://localhost:8000/
### To delete container
```
docker-compose down -v
```
### Administrator DB migrate
```
python manage.py makemigrations administrator
python manage.py migrate administrator --database=administrator_db
```
***
## Production
### Finish generic setup
### In your .env file add this line
```
DEBUG = False
```
***
## Development
### To run tests
```
pytest
```
### Pre-commit command
```
pre-commit run --all-files
```

### Technology

- Python 3
- Django REST Framework
- Django
- Celery
- SimleJWT
- Docker
- PostgreSQL
- SQLite
- Bootstrap
