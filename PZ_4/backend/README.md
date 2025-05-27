# Financial Analysis API

API для анализа финансовых данных с использованием машинного обучения.

## Требования

- Python 3.8+
- PostgreSQL 12+
- Redis (опционально, для кэширования)

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd PZ_4/backend
```

2. Создайте виртуальное окружение:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории backend:
```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=financial_analysis
SECRET_KEY=your-secret-key-here
```

5. Создайте базу данных PostgreSQL:
```sql
CREATE DATABASE financial_analysis;
```

## Инициализация базы данных

1. Убедитесь, что PostgreSQL запущен и доступен

2. Запустите скрипт инициализации:
```bash
python -m app.db.init_db_script
```

Это создаст:
- Все необходимые таблицы
- Суперпользователя (admin@example.com / admin)
- Тестовые финансовые данные

## Запуск приложения

1. Запустите сервер разработки:
```bash
uvicorn app.main:app --reload
```

2. API будет доступно по адресу: http://localhost:8000

3. Документация API доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Использование API

1. Регистрация нового пользователя:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123", "full_name": "Test User"}'
```

2. Получение токена доступа:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "user@example.com", "password": "password123"}'
```

3. Использование API с токеном:
```bash
curl -X GET "http://localhost:8000/api/v1/financial/data" \
     -H "Authorization: Bearer your_access_token"
```

## Структура проекта

```
backend/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core functionality
│   ├── crud/           # Database operations
│   ├── db/             # Database configuration
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic models
│   └── services/       # Business logic
├── tests/              # Test files
├── .env               # Environment variables
├── requirements.txt   # Project dependencies
└── README.md         # This file
```

## Разработка

1. Установите зависимости для разработки:
```bash
pip install -r requirements-dev.txt
```

2. Запустите тесты:
```bash
pytest
```

## Возможные проблемы и решения

1. Ошибка подключения к PostgreSQL:
   - Убедитесь, что PostgreSQL запущен
   - Проверьте правильность учетных данных в .env
   - Проверьте, что база данных создана

2. Ошибка импорта модулей:
   - Убедитесь, что вы находитесь в корневой директории проекта
   - Проверьте, что виртуальное окружение активировано

3. Ошибка при инициализации базы данных:
   - Удалите существующую базу данных и создайте новую
   - Проверьте права доступа пользователя PostgreSQL

## Лицензия

MIT 