# test_parser

# Apteka April Parser

## Описание

Парсер для сбора информации о товарах с сайта аптеки "Апрель" с использованием Scrapy и Python 3.12. Данные отправляются в RabbitMQ и обрабатываются сервисом на FastStream для сохранения в PostgreSQL.

## Установка

### Требования

- Docker
- Docker Compose
- Python 3.12
- Poetry

### Шаги установки

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/apteka_april_parser.git
   cd apteka_april_parser


---

### **7. Стратегия обхода блокировок**

Мы используем следующие методы для обхода блокировок:

- **Имитация реального пользователя:** Устанавливаем заголовок `User-Agent` в настройках Scrapy.
- **Регулирование скорости запросов:** Используем `DOWNLOAD_DELAY` и `AUTOTHROTTLE` для управления скоростью запросов и снижения нагрузки на сервер.
- **Повторные попытки:** Настроены параметры `RETRY_ENABLED` и `RETRY_TIMES` для повторных попыток при неудачных запросах.
- **Обработка ошибок:** Логируем ошибки и исключения для последующего анализа и улучшения парсера.

**Обоснование выбора:** Эти методы позволяют эффективно собирать данные, минимизируя вероятность блокировки со стороны сервера и обеспечивая устойчивую работу парсера.

---

## **Дополнительные задания**

### **1. Уведомления через Telegram**

#### **Реализация**

- Используем библиотеку **python-telegram-bot**.
- Создаем бота и получаем токен.
- Добавляем в парсер отправку уведомлений при старте, завершении и возникновении ошибок.

#### **Код**

```python
# В main.py
import logging
from telegram import Bot

TELEGRAM_TOKEN = 'your-telegram-token'
CHAT_ID = 'your-chat-id'

def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == '__main__':
    try:
        send_telegram_message('Парсер запущен')
        run_spider(args.city_ids)
        send_telegram_message('Парсер успешно завершен')
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        send_telegram_message(f'Ошибка при работе парсера: {e}')
