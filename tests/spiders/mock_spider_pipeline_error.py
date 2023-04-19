import scrapy
from base_crawler.spiders.base_spider import BaseSpider


class MockSpiderPipelineError(BaseSpider):
    name = "mock-spider-pipeline-error"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["failKey"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = {"a": "b"}

    def start_requests(self):
        yield scrapy.Request(url="http://example.com", callback=self.parse)

    def parse(self, response):
        yield {"testKey": "testvalue"}
