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

1. Клонируйте репозиторий:

   git clone https://github.com/PoGen-dev/test_parser

2. Устанавливаем все библиотеки через poetry

3. Скачать chromedriver и chrome для Вашей OS с https://googlechromelabs.github.io/chrome-for-testing/

4. Создать в корневой папке проекта папку resourse и переместить туда папки из zip архивой от chromedriver и chrome

5. Установить и развернуть RabbitMQ и Postgres

6. Создать базу данных в Postgres с названием products_db. Создать таблицу в бд


```sql -- CREATE TABLE products (product_id VARCHAR PRIMARY KEY,name TEXT,price NUMERIC,special_price NUMERIC,manufacturer TEXT,country TEXT);```

7. Запускаем парсер используя команду (не забудьте передать id городов)

```bash -- poetry run python main -c 1 721```

8. Запускаем FastStream используя команду

```bash -- poetry run python faststream_service\faststream_main.py```

### Стратегия обхода блокировок

Мы используем следующие методы для обхода блокировок:

- **Имитация реального пользователя:** Устанавливаем заголовок `User-Agent` в настройках Scrapy.
- **Регулирование скорости запросов:** Используем `DOWNLOAD_DELAY` и `AUTOTHROTTLE` для управления скоростью запросов и снижения нагрузки на сервер.
- **Повторные попытки:** Настроены параметры `RETRY_ENABLED` и `RETRY_TIMES` для повторных попыток при неудачных запросах.
- **Обработка ошибок:** Логируем ошибки и исключения для последующего анализа и улучшения парсера.

**Обоснование выбора:** Эти методы позволяют эффективно собирать данные, минимизируя вероятность блокировки со стороны сервера и обеспечивая устойчивую работу парсера.
