import asyncio
import json
import asyncpg
import pika
from pydantic import BaseModel


class Product(BaseModel):
    product_id: int
    name: str
    price: float
    special_price: float = None
    manufacturer: str
    country: str


async def save_to_db(pool, data):
    async with pool.acquire() as connection:
        await connection.execute(
            """
            INSERT INTO products (product_id, name, price, special_price, manufacturer, country)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (product_id) DO NOTHING;
        """,
            data.product_id,
            data.name,
            data.price,
            data.special_price,
            data.manufacturer,
            data.country,
        )


async def consume():
    params = pika.URLParameters("amqp://guest:guest@localhost:5672/")
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue="products", durable=True)

    pool = await asyncpg.create_pool(
        user="postgres", password="postgres", database="products_db", host="postgres"
    )

    def callback(ch, method, properties, body):
        for i in range(3):
            try:
                message = json.loads(body)
                data = Product(**message)
                asyncio.create_task(save_to_db(pool, data))
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            except Exception as e:
                ...

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="products", on_message_callback=callback)
    channel.start_consuming()


if __name__ == "__main__":
    asyncio.run(consume())
