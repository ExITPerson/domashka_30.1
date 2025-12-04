# Django + Celery + Docker

Полноценный Django-проект с асинхронными задачами (Celery), периодическими заданиями (Celery Beat), кэшированием (Redis) и базой данных (PostgreSQL), полностью контейнеризованный в Docker.

---

## 📋 Предварительные требования

- **Docker** (версия 20.10 или выше)
- **Docker Compose** (версия 2.0 или выше)
- Git (для клонирования репозитория)

---

## 🚀 Быстрый старт

### 1. Клонирование проекта
```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd domashka_30.1
```

### 2. Настройка переменных окружения
Скопируйте файл `.env.sample` в `.env` и заполните необходимые значения:

```bash
cp .env.sample .env
```

Откройте файл `.env` и обязательно укажите:
- `SECRET_KEY` — секретный ключ Django (можно сгенерировать онлайн)
- `POSTGRES_DB=school` — имя базы данных
- `POSTGRES_USER=school_user` — пользователь БД
- `POSTGRES_PASSWORD=school_password` — пароль пользователя
- `POSTGRES_HOST=db` — хост базы данных (имя сервиса из docker-compose)
- `POSTGRES_PORT=5432` — порт базы данных
- `CELERY_BROKER_URL=redis://redis:6379/0` — URL Redis для Celery
- `CELERY_RESULT_BACKEND=redis://redis:6379/0` — бекенд результатов Celery

### 3. Запуск проекта
```bash
docker-compose up -d
```

Команда **соберет Docker-образы, запустит все сервисы и применит миграции**.

---

## 🔍 Проверка работоспособности сервисов

### 1. **Django (Web)**
**Проверка:**
```bash
# Через curl
curl http://localhost:8000

# Через браузер
# Откройте http://localhost:8000
```

**Ожидаемый результат:**  
- HTTP-ответ 200
- Страница Django (или ваша кастомная страница) загружается

**Проверка логов:**
```bash
docker-compose logs web -f
```
Должно быть: `Watching for file changes with StatReloader`

---

### 2. **PostgreSQL (База данных)**
**Проверка:**
```bash
docker-compose logs db -f
```

**Ожидаемый результат:**
```
database system is ready to accept connections
```

**Проверка подключения изнутри контейнера:**
```bash
docker-compose exec db psql -U school_user -d school -c "SELECT 1;"
```
Должно вернуть: `1`

---

### 3. **Redis**
**Проверка:**
```bash
docker-compose logs redis -f
```

**Ожидаемый результат:**
```
Ready to accept connections tcp
```

**Проверка работы через CLI:**
```bash
docker-compose exec redis redis-cli ping
```
Должно вернуть: `PONG`

---

### 4. **Celery Worker**
**Проверка:**
```bash
docker-compose logs celery -f
```

**Ожидаемый результат:**
```
celery@<id> ready.
[tasks]
  . materials.tasks.update_notification
  . users.tasks.deactivate_inactive_users
```

**Проверка выполнения задачи (из контейнера web):**
```bash
docker-compose exec web python manage.py shell
# В консоли Django:
>>> from users.tasks import deactivate_inactive_users
>>> deactivate_inactive_users.delay()
# Должен вернуться ID задачи
```

---

### 5. **Celery Beat (Периодические задачи)**
**Проверка:**
```bash
docker-compose logs celery-beat -f
```

**Ожидаемый результат:**
```
beat: Starting...
DatabaseScheduler: Schedule changed.
```
Это означает, что Beat успешно подключился к БД и загрузил расписание.

**Проверка расписания (если есть периодические задачи):**
```bash
docker-compose exec web python manage.py shell
# В консоли Django:
>>> from django_celery_beat.models import PeriodicTask
>>> PeriodicTask.objects.all().count()
# Должен вернуть количество настроенных задач
```

---

## 🛠️ Дополнительные команды

### Создание суперпользователя Django
```bash
docker-compose exec web python manage.py createsuperuser
```

### Применение миграций (если вносили изменения)
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Остановка проекта
```bash
docker-compose down
```

### Полная очистка (контейнеры, тома, сети)
```bash
docker-compose down -v
```

---

## 📁 Структура проекта

```
domashka_30.1/
├── app/                    # Приложение Django
├── config/                 # Настройки проекта
├── fixtures/               # Фикстуры
├── materials/              # Приложение materials
├── static/                 # Статические файлы
├── users/                  # Приложение users
├── .env.sample            # Шаблон переменных окружения
├── docker-compose.yml     # Конфигурация Docker Compose
├── Dockerfile             # Dockerfile для web/celery/celery-beat
├── requirements.txt       # Python-зависимости
└── manage.py              # manage.py Django
```

---

## 📝 Примечания

- **Порт 8000** - Django web-сервер
- **Порт 5432** - PostgreSQL (можно подключаться через DBeaver, pgAdmin)
- **Порт 6379** - Redis (можно подключаться через Redis Insight)
- Все сервисы запускаются с помощью одной команды `docker-compose up -d`
- Для продакшена рекомендуется убрать `DEBUG=True` и настроить хосты в `ALLOWED_HOSTS`