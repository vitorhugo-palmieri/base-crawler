import scrapy
from base_crawler.spiders.base_spider import BaseSpider
from base_crawler.exceptions.spider_exceptions import InputNotFound
from base_crawler.exceptions.spider_exceptions import InvalidPage
from base_crawler.exceptions.spider_exceptions import InvalidInput


class MockSpiderNotFound(BaseSpider):
    name = "mock-spider-not-found"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["testKey"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = {"a": "b"}

    def start_requests(self):
        yield scrapy.Request(url="http://example.com", callback=self.parse)

    def parse(self, response):
        raise InputNotFound()


class MockSpiderInvalidPage(BaseSpider):
    name = "mock-spider-invalid-page"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["testKey"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = {"a": "b"}

    def start_requests(self):
        yield scrapy.Request(url="http://example.com", callback=self.parse)

    def parse(self, response):
        raise InvalidPage()


class MockSpiderInvalidInput(BaseSpider):
    name = "mock-spider-invalid-input"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["testKey"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = kwargs["input"]

    def start_requests(self):
        yield scrapy.Request(url="http://example.com", callback=self.parse)

    def parse(self, response):
        raise InvalidInput(self.input)
