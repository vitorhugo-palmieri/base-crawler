from http import HTTPStatus

import scrapy

from base_crawler.spiders.base_spider import BaseSpider
from base_crawler.bucket.oci_bucket import OracleBucketManager

from tests import test_helper


class MockSpiderUploadText(BaseSpider):
    name = "mock-spider-upload-text"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["testKey"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = {"a": "b"}

    def start_requests(self):
        self.logger.info("START REQUESTS UPLOAD TEXT")
        self.bucket_manager = OracleBucketManager()
        yield scrapy.Request(url="https://www.google.com", callback=self._on_first_page)

    def _on_first_page(self, response):
        self.logger.info("FIRST PAGE UPLOAD TEXT")
        file_content = test_helper.read_test_file("test_file.txt")
        file_name = "test_file.txt"

        yield self.bucket_manager.create_put_bucket_request(
            file_content=file_content,
            file_name=file_name,
            callback=self._on_success_upload,
            errback=None,
        )

    def _on_success_upload(self, response):
        assert response.status == HTTPStatus.OK

        return {"testKey": "testvalue"}


class MockSpiderUploadPdf(BaseSpider):
    name = "mock-spider-upload-pdf"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["testKey"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = {"a": "b"}

    def start_requests(self):
        self.logger.info("START REQUESTS UPLOAD PDF")
        self.bucket_manager = OracleBucketManager()
        yield scrapy.Request(url="https://www.google.com", callback=self._on_first_page)

    def _on_first_page(self, response):
        self.logger.info("FIRST PAGE UPLOAD PDF")
        file_content = test_helper.read_test_file("test_file.pdf")
        file_name = "test_file.pdf"

        yield self.bucket_manager.create_put_bucket_request(
            file_content=file_content,
            file_name=file_name,
            callback=self._on_success_upload,
            errback=None,
        )

    def _on_success_upload(self, response):
        assert response.status == HTTPStatus.OK

        return {"testKey": "testvalue"}


class MockSpiderUploadHtml(BaseSpider):
    name = "mock-spider-upload-html"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["testKey"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = {"a": "b"}

    def start_requests(self):
        self.logger.info("START REQUESTS UPLOAD HTML")
        self.bucket_manager = OracleBucketManager()
        yield scrapy.Request(url="https://www.google.com", callback=self._on_first_page)

    def _on_first_page(self, response):
        self.logger.info("FIRST PAGE UPLOAD HTML")
        file_content = test_helper.read_test_file("test_file.html")
        file_name = "test_file.html"

        yield self.bucket_manager.create_put_bucket_request(
            file_content=file_content,
            file_name=file_name,
            callback=self._on_success_upload,
            errback=None,
        )

    def _on_success_upload(self, response):
        assert response.status == HTTPStatus.OK

        return {"testKey": "testvalue"}
