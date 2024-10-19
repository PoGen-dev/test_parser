# Apteka April Parser

## Описание

Парсер для сбора информации о товарах с сайта аптеки "Апрель" с использованием Scrapy и Python 3.12. Данные отправляются в RabbitMQ и обрабатываются сервисом на FastStream для сохранения в PostgreSQL.

## Установка

### Требования

- Python 3.12
- Poetry
- Postgres
- RabbitMQ

### Шаги установки

1. Клонирование репозитория:

   git clone https://github.com/PoGen-dev/test_parser

2. Установка всех библиотеки через poetry

3. Скачивание chromedriver и chrome для Вашей OS с https://googlechromelabs.github.io/chrome-for-testing/

4. Создание в корневой папке проекта папку resourse и перемещение туда папки из zip архивой от chromedriver и chrome

5. Установка и развёртка RabbitMQ и Postgres

6. Создание базы данных в Postgres с названием products_db. Создание таблицы в бд

```CREATE TABLE products (product_id VARCHAR PRIMARY KEY,name TEXT,price NUMERIC,special_price NUMERIC,manufacturer TEXT,country TEXT);```

7. (Опционально) Указать токен от телеграм бота и id чата куда необходимо присылать письма в \apteka_parser\settings.py

8. Запуск парсер используя команду (не забудьте передать id городов)

```poetry run python main -c 1 721```

9. Запуск FastStream используя команду

```poetry run python faststream_service\faststream_main.py```

### Конфигурация RabbitMQ

- RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
- RABBITMQ_QUEUE = "products"
- RABBITMQ_DEFAULT_USER = "guest"
- RABBITMQ_DEFAULT_PASS = "guest"
- PORT = 5672

### Стратегия обхода блокировок

Мы используем следующие методы для обхода блокировок:

- **Имитация реального пользователя:** Устанавливаем заголовок `User-Agent` в настройках Scrapy.
- **Регулирование скорости запросов:** Используем `DOWNLOAD_DELAY` и `AUTOTHROTTLE` для управления скоростью запросов и снижения нагрузки на сервер.
- **Повторные попытки:** Настроены параметры `RETRY_ENABLED` и `RETRY_TIMES` для повторных попыток при неудачных запросах.
- **Обработка ошибок:** Логируем ошибки и исключения для последующего анализа и улучшения парсера.

**Обоснование выбора:** Эти методы позволяют эффективно собирать данные, минимизируя вероятность блокировки со стороны сервера и обеспечивая устойчивую работу парсера.


### Пример полученных данных

- {"product_id": 291847, "name": "\u041d\u043e\u0441\u043a\u0438 \u0436\u0435\u043d\u0441\u043a\u0438\u0435 \u0441 \u043c\u0438\u0448\u043a\u0430\u043c\u0438 \u0440\u0430\u0437\u043c\u0435\u0440 23-25", "price": 87, "special_price": 87, "country": "\u0420\u043e\u0441\u0441\u0438\u044f", "manufacturer": "\u041e\u041e\u041e \"\u0410\u0432\u0440\u043e\u0440\u0430 \u0410\u043b\u0442\u0430\u044f\""}
- {"product_id": 235471, "name": "\u041f\u043e\u0434\u0441\u043b\u0435\u0434\u043d\u0438\u043a\u0438 \u0436\u0435\u043d\u0441\u043a\u0438\u0435 \u0441\u0435\u0440\u044b\u0435 \u0440.23-25", "price": 78, "special_price": 78, "country": "\u0420\u043e\u0441\u0441\u0438\u044f", "manufacturer": "\u0410\u041e \"\u0411\u043e\u0440\u0438\u0441\u043e\u0433\u043b\u0435\u0431\u0441\u043a\u0438\u0439 \u0442\u0440\u0438\u043a\u043e\u0442\u0430\u0436\""}
- {"product_id": 235472, "name": "\u041f\u043e\u0434\u0441\u043b\u0435\u0434\u043d\u0438\u043a\u0438 \u0436\u0435\u043d\u0441\u043a\u0438\u0435 \u0447\u0435\u0440\u043d\u044b\u0435 \u0440.23-25", "price": 78, "special_price": 78, "country": "\u0420\u043e\u0441\u0441\u0438\u044f", "manufacturer": "\u0410\u041e \"\u0411\u043e\u0440\u0438\u0441\u043e\u0433\u043b\u0435\u0431\u0441\u043a\u0438\u0439 \u0442\u0440\u0438\u043a\u043e\u0442\u0430\u0436\""}
