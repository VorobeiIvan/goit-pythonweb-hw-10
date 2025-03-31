FROM python:3.11-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN useradd -m appuser

WORKDIR /app

COPY ../requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . .

RUN chmod +x /app/start.sh
RUN chown -R appuser:appuser /app

USER appuser

CMD ["/app/start.sh"]
