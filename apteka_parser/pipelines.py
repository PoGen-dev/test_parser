# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pika
import json
from typing import Any
from itemadapter import ItemAdapter


class RabbitMQPipeline:
    def __init__(self, rabbitmq_url, queue_name) -> None:
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            rabbitmq_url=crawler.settings.get("RABBITMQ_URL"),
            queue_name=crawler.settings.get("RABBITMQ_QUEUE"),
        )

    def open_spider(self, spider) -> None:
        """
        Action on open spider

        :param spider:
        :return None:
        """
        params = pika.URLParameters(self.rabbitmq_url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def close_spider(self, spider) -> None:
        """
        Action on close spider

        :param spider:
        :return None:
        """
        self.connection.close()

    def process_item(self, item, spider) -> Any:
        """
        Send item to the RabbitMQ

        :param item:
        :param spider:
        :return Any:
        """
        adapter = ItemAdapter(item)
        message = json.dumps(adapter.asdict())
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
        return item
