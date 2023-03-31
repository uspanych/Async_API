# Сервис Async API

## Структура проекта:

* etl - Сервис для синхронизации записей Postgres -> Elasticsearch.
* API service - Сервис для предоставления интерфейса взаимодействия с системой.


## Докумнтация

Документация методов доступна в [OpenAPI](http://localhost:8000/api/openapi) после разворачивания сервиса.


## Используемые технологии

1. В качестве фреймворка используется [FastAPI](https://fastapi.tiangolo.com/)
2. Для увеличесния быстродействия приложения используется кэширование, основанное на [Redis](https://redis.io/)
3. Для хранения данных используется реляционная БД [PostgreSQL](https://www.postgresql.org/)
4. Для гибкого поиска используется документоориентированная БД [Elasticsearch](https://www.elastic.co/)
5. Для удобства разворачивания/использования используется [Docker](https://www.docker.com/)


## Установка

### Для установки необходимо выполнить следующие шаги:
1. Склонировать данный [репозиторий](https://github.com/uspanych/Async_API).
2. Создать файл ```.env```.
3. Заполнить файл ```.env``` как показано в ```.env.example```, заменяя значения на свои.
4. Запустить проект командой ```docker-compose up -d --build```.
