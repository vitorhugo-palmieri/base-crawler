import os
import json

import pika
from base_crawler.exceptions import rabbit_exceptions
from base_crawler import helper


class RabbitPipeline:
    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=helper.get_rabbit_host(),
                    heartbeat=3600,
                    credentials=helper.get_rabbit_credentials(),
                )
            )
            self.channel = self.connection.channel()
        except:
            raise rabbit_exceptions.RabbitConnectionException()

    def _connect(self, queue_name):
        try:
            self.queue = self.channel.queue_declare(
                queue=f"{queue_name}_outputs", durable=True
            )
        except Exception as e:
            self.connection.close()
            raise rabbit_exceptions.QueueDeclarationException(str(e))

    def process_item(self, item, spider):
        self._connect(spider.name)
        self.channel.basic_publish(
            exchange="", routing_key=f"{spider.name}_outputs", body=json.dumps(item)
        )
        spider.logger.info(f"Sent item to rabbit queue {spider.name}_outputs - {item}")
        return item
