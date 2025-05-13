# Используем официальный Python образ в качестве базового
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем сначала зависимости для лучшего кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Затем копируем остальные файлы проекта
COPY . /app

# Обеспечиваем unbuffered вывод логов
ENV PYTHONUNBUFFERED=1

# Открываем порт, который будет использовать FastAPI
EXPOSE 8000

# Запускаем сервер через Uvicorn
CMD ["python", "app.py"]