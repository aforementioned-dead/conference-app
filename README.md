# Система управления конференциями

Веб-приложение для управления конференциями, позволяющее пользователям регистрироваться, планировать и просматривать доклады. Проект демонстрирует использование **FastAPI**, **PostgreSQL**, **SQLAlchemy** и других технологий.

## Возможности
- **Пользователи:** Роли - Докладчик (Presenter) и Слушатель (Listener).
- **Докладчики:**
  - Создание и управление докладами.
  - Планирование докладов в аудиториях без пересечения по времени.
- **Слушатели:**
  - Просмотр расписания конференции.
  - Регистрация на доклады.
- **REST API:** Доступная документация через Swagger UI.

## Используемые технологии
- **FastAPI**: Фреймворк для backend-разработки.
- **PostgreSQL**: СУБД.
- **SQLAlchemy**: ORM для взаимодействия с базой данных.
- **Alembic**: Миграции базы данных.
- **Pytest**: Автоматическое тестирование.
- **Docker**: Контейнеризация.

## Начало работы

### Предварительные требования
- **Python 3.10+**
- **Docker** 

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/aforementioned-dead/conference-app.git
   cd conference-app

2. Создайте и активируйте виртуальное окружение:
   ```
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate

4. Установите зависимости:
   ```
   poetry install

5. Настройте базу данных:
   Создайте базу данных PostgreSQL и обновите переменную DATABASE_URL в файле .env   
   Примените миграции:
   ```
   alembic upgrade head

### Запуск приложения
1. Запустите сервер:
   ```
   uvicorn main:app --reload

2. Откройте Swagger UI:
   - Перейдите по адрему http://127.0.0.1:8000/docs
   
3. Изучите API

### Запуск с использованием Docker
1. Соберите и запустите контейнер Docker:
   ```
   docker-compose up --build

2. Перейдите в conference_app:
   ```
   docker exec -it conference_app bash
   
3. Доступ к приложению http://localhost:8000/docs

### Тестирование
1. Запустите все тесты:
   ```
   poetry run pytest

2. Убедитесь, что все тесты проходят успешно

### API Эндпоинты
Аудитории (Rooms):
   - POST /rooms: Создать аудиторию
   - GET /rooms: Получить список всех аудиторий
   - PUT /rooms/{room_id}: Обновить созданную комнату
   - DELETE /rooms/{room_id}: Удалить комнату

Доклады (Presentations):
   - POST /presentations: Создать доклад
   - GET /presentations: Получить список всех докладов
   - PUT /presentations/{presentation_id}: Обновить доклад
   - DELETE /presentations/{presentation_id}: Удалить доклад по его ID

Расписание (Schedules)
   - POST /schedules: Запланировать доклад
   - GET /schedule-by-room: Просмотреть расписание, сгруппированное по аудиториям
   - GET /schedules: Получить список всех расписаний
   - PUT /schedules/{schedule_id}: Обновить расписание
   - DELETE /schedules/{schedule_id}: Удалить расписание

Пользователи (Users):
   - GET /users: Получить список всех пользователей
   - POST /users: Создать нового пользователя
   - PUT /users/{user_id}: Обновить данные пользователя
   - DELETE /users/{user_id}: Удалить пользователя

### Примеры данных
Создание аудитории:
{
    "name": "Большой зал"
}

Создание доклада:
{
    "title": "Перенаселение планеты",
    "description": "Как остановить этот процесс",
    "presenter": "Грета Тунберг"
}

Планирование доклада:
{
    "room_id": 1,
    "presentation_id": 1,
    "start_time": "2025-01-16T10:00:00",
    "end_time": "2025-01-16T11:00:00"
}

