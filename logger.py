import logging
import os
from logging.handlers import RotatingFileHandler

# Создаем объект логгера
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

# Создаем форматтер для логов
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Создаем обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Создаем обработчик для записи логов в файл
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)  # Создаем директорию для логов
file_handler = RotatingFileHandler(
    os.path.join(log_directory, "app.log"),
    maxBytes=1024 * 1024,  # 1 MB
    backupCount=5          # Сохраняем последние 5 файлов
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(console_handler)
logger.addHandler(file_handler)