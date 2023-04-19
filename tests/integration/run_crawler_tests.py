import pika
import unittest
from crochet import setup
from run_crawler import CrawlerInputRabbit

from base_crawler import helper


class RunCrawlerTests(unittest.TestCase):
    def setUp(self):
        self.crawler_input = CrawlerInputRabbit()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=helper.get_rabbit_host(),
                heartbeat=3600,
                credentials=helper.get_rabbit_credentials(),
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="mock-spider-success_inputs", durable=True)

    def tearDown(self):
        self.channel.close()
        self.connection.close()

    def test_produce_input_correctly(self):
        self.channel.basic_publish(
            exchange="",
            routing_key=f"mock-spider-success_inputs",
            body=b'{"testKey":"testvalue"}',
        )
        self.channel.basic_publish(
            exchange="", routing_key=f"mock-spider-success_inputs", body="exit".encode()
        )
        self.crawler_input.run_crawler("mock-spider-success")
        self.assertEqual(2, self.crawler_input.queue.method.message_count)


if __name__ == "__main__":
    setup()
    unittest.main()
