```markdown
<!-- README.md -->
# 🧠 Додаток FastAPI + PostgreSQL

Це веб-додаток, створений за допомогою FastAPI та PostgreSQL, повністю контейнеризований за допомогою Docker Compose. Він підтримує гаряче перезавантаження для розробки та має модульну структуру для масштабованості.

## 🚀 Технологічний стек

- **FastAPI** – сучасний, високопродуктивний веб-фреймворк для створення API.
- **PostgreSQL** – реляційна база даних.
- **Docker та Docker Compose** – контейнеризація додатка для зручності розгортання.
- **SQLAlchemy** – ORM для зручної роботи з базою даних.
- **Pydantic** – валідація та серіалізація даних.
- **Cloudinary** – збереження медіафайлів.
- **Python-dotenv** – для завантаження змінних середовища.

---

## ⚙️ Інструкції з налаштування

### 1️⃣ Клонування репозиторія
```bash
git clone https://github.com/your-repository/goit-pythonweb-hw-10
cd goit-pythonweb-hw-10
```

### 2️⃣ Налаштування змінних середовища
Скопіюйте приклад файлу змінних середовища:

```bash
cp .env.example .env
```

Потім заповніть `.env` своїми значеннями:

```
SECRET_KEY=<Ваш секретний ключ>
DATABASE_URL=<URL підключення до PostgreSQL>
CLOUDINARY_URL=<Ваш Cloudinary URL>
CLOUDINARY_CLOUD_NAME=<Ім'я хмари Cloudinary>
CLOUDINARY_API_KEY=<Ключ API Cloudinary>
CLOUDINARY_API_SECRET=<Секрет API Cloudinary>
ALGORITHM=<Алгоритм для JWT, наприклад HS256>
ACCESS_TOKEN_EXPIRE_MINUTES=<Час життя токена у хвилинах>
SMTP_SERVER=<SMTP сервер для email>
SMTP_PORT=<Порт SMTP>
SMTP_EMAIL=<Email для відправлення листів>
SMTP_PASSWORD=<Пароль для email>
POSTGRES_USER=<Користувач PostgreSQL>
POSTGRES_PASSWORD=<Пароль PostgreSQL>
POSTGRES_DB=<Назва бази даних PostgreSQL>
```

### 3️⃣ Запуск проєкту
Забезпечте, щоб Docker був встановлений на вашій машині. Потім виконайте:

```bash
docker-compose up --build
```

API буде доступний за адресою: [http://localhost:8000](http://localhost:8000)

---

## 📫 API Ендпоінти

FastAPI надає інтерактивну документацію, яка доступна за посиланнями:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔑 Основні функціональні можливості

- **Авторизація**: Реєстрація, вхід, підтвердження email, генерація токенів доступу.
- **Робота з контактами**:
    - Створення, перегляд, оновлення та видалення контактів.
    - Пошук контактів із днями народження, які наближаються.
- **Завантаження медіафайлів**: Використання Cloudinary для роботи з аватарками користувачів.

---

## 🧪 Тестування

Додаток підтримує тестування API:

1. Встановіть залежності для тестування:

```bash
pip install pytest pytest-asyncio
```

2. Запустіть тести:

```bash
pytest
```

---

## 🛠 Форматування коду

Для форматування коду використовуйте `black`:

```bash
black .
```

---

## 📂 Структура проєкту

```plaintext
.
├── README.md
├── docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── start.sh
├── env
│   └── .env.example
├── requirements.txt
├── setup.cfg
└── src
        ├── config
        │   ├── config.py              # Конфігурація змінних середовища
        │   ├── logging_config.py      # Логування
        │   └── security_config.py     # Безпека (хешування паролів)
        ├── constants
        │   ├── auth.py                # Налаштування аутентифікації
        │   ├── consts.py              # Глобальні константи
        │   └── security.py            # Безпека
        ├── database
        │   └── database.py            # Налаштування бази даних (PostgreSQL)
        ├── main.py                    # Точка входу до додатку
        ├── middleware
        │   └── middleware.py          # Middleware для перевірки змінних середовища
        ├── models
        │   └── models.py              # ORM моделі для бази даних
        ├── routers
        │   ├── auth.py                # Роутинг для авторизації
        │   ├── contacts.py            # Роутинг для роботи з контактами
        │   └── users.py               # Роутинг для профілю користувача
        ├── schemas
        │   └── contact.py             # Pydantic-схеми
        ├── utils
        │   ├── auth
        │   │   ├── auth_utils.py      # Допоміжні функції для авторизації
        │   │   ├── passwords.py       # Хешування паролів
        │   │   └── tokens.py          # Генерація та валідація токенів
        │   ├── db
        │   │   └── sessions.py        # Сесії бази даних
        │   ├── email
        │   │   └── send_email.py      # Відправка листів
        │   └── key_generator.py       # Генерація ключів
        └── validators
                ├── validate_birthday.py   # Валідація дати народження
                └── validate_phone_number.py # Валідація номерів телефонів
```

---

## 🛡 Безпека

- Використання `bcrypt` для хешування паролів.
- JWT для автентифікації користувачів.
- Перевірка змінних середовища під час запуску додатка.

---

## 📧 Контакти

Якщо у вас є запитання чи пропозиції, напишіть на `your-email@example.com`.
```
