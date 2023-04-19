import os
import sys
import json
import logging
import threading

import pika
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from crochet import setup

from base_crawler import helper
from base_crawler.exceptions import rabbit_exceptions

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_concurrencies = int(os.environ.get("CONCURRENCY_COUNT", "3"))

if not _concurrencies:
    _concurrencies = 3


class CrawlerInputRabbit:
    """
    This class represents a crawler that receives an input from RabbitMQ.

    The crawler instantiates a CrawlerRunner and adds the self._finish_crawl method to the deferred callback.

    When the crawler returns, either by finishing an input or by raising an exception, the deferred callback (self._finish_crawl) is executed.

    The crochet library is used to make the Twisted reactor work when running multiple crawlers simultaneously.

    The concurrency count environment variable is used as the maximum semaphore size, to control crawler creation,
    and it's also used as the prefetch count in RabbitMQ, to ensure that only this number of messages will be consumed from the queue at a time.
    """

    def __init__(self):
        """
        The crawler is constructed by creating a connection to RabbitMQ and the semaphore.
        """
        super().__init__()
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=helper.get_rabbit_host(),
                    heartbeat=3600,
                    credentials=helper.get_rabbit_credentials(),
                )
            )
            self.channel = self.connection.channel()
            self.semaphore = threading.Semaphore(_concurrencies)
        except:
            logger.error("RabbitMQ Error")
            raise rabbit_exceptions.RabbitConnectionException()

    def _on_received_message(self, ch, method, properties, body):
        """
        This function is the callback executed when a message from RabbitMQ is received.

        It creates a new CrawlerRunner and initiates crawling. When the crawler ends, the deferred callback is executed.
        """
        logger.debug(f"Received message is {body}")
        if body.decode() == "exit":
            logger.info("Exit message received, will stop consuming from queue")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.stop_consuming()
            return

        spider_input = json.loads(body.decode())
        logger.debug(f"Input is {spider_input}")
        self.semaphore.acquire()
        logger.debug("********* LOCK ACQUIRED *********")
        process = CrawlerRunner(settings=get_project_settings())
        process.crawl(self.spider_name, args=[], input=spider_input)
        deferred_crawl = process.join()
        deferred_crawl.addBoth(self._finish_crawl)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run_crawler(self, spider_name=""):
        """
        This function gets the queue name from the argument in the Dockerfile entrypoint, declares the queue and starts consumption.
        """
        command_line_args = sys.argv[1:]
        if spider_name == "":
            for i in range(0, len(command_line_args), 2):
                if "-name" in command_line_args[i]:
                    spider_name = command_line_args[i].split("=")[1]
                    break
        logger.info(f"Spider name is {spider_name}")
        self.spider_name = spider_name
        logger.info(f"Will consume from queue {spider_name}_inputs")
        self.queue = self.channel.queue_declare(
            queue=f"{spider_name}_inputs", durable=True
        )
        self.channel.basic_consume(
            queue=f"{spider_name}_inputs",
            on_message_callback=self._on_received_message,
            auto_ack=False,
        )
        self.channel.basic_qos(prefetch_count=_concurrencies)
        self.channel.start_consuming()
        # self.channel.close()

    def _finish_crawl(self, result):
        """
        This is the deferred callback, executed when a crawler finishes execution.

        Because it is added using the "addBoth" method, this method is executed whether the crawler finishes successfully or not.

        The only purpose of this function is to release a position in the semaphore to allow the next crawler to be instantiated.
        """
        logger.info("Running crawler finished")
        self.semaphore.release()


if __name__ == "__main__":
    setup()
    crawler_rabbit = CrawlerInputRabbit()
    crawler_rabbit.run_crawler()
