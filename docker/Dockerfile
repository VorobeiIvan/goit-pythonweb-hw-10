# Використовуємо офіційний легковаговий образ Python
FROM python:3.11-slim

# Додаємо користувача для безпечного запуску контейнера
RUN useradd -m appuser

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо та встановлюємо залежності (оптимізуємо кешування)
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Копіюємо решту коду
COPY . .

# Робимо `start.sh` виконуваним
RUN chmod +x /start.sh

# Змінюємо власника файлів на створеного користувача
RUN chown -R appuser:appuser /app

# Переключаємось на безпечного користувача
USER appuser

# Запускаємо FastAPI через `start.sh`
CMD ["/start.sh"]
