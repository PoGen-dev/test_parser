# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pika
import json
from itemadapter import ItemAdapter


class RabbitMQPipeline:
    def __init__(self, rabbitmq_url, queue_name):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            rabbitmq_url=crawler.settings.get('RABBITMQ_URL'),
            queue_name=crawler.settings.get('RABBITMQ_QUEUE')
        )

    def open_spider(self, spider):
        params = pika.URLParameters(self.rabbitmq_url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        message = json.dumps(adapter.asdict())
        with open('example.json', 'a', encoding='utf-8') as f:
            json.dump(adapter.asdict(), f)
            f.write('\n')
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        return item
