import sys

from loguru import logger

# Удаляем все существующие обработчики
logger.remove()

# Настройка логирования
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> - "
    "<level>{level:^8}</level> - "
    "<cyan>{name}</cyan>:<magenta>{line}</magenta> - "
    "<yellow>{function}</yellow> - "
    "<white>{message}</white>",
)
