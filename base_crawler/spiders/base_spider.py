import json
import os
from scrapy import Spider
from base_crawler.exceptions.spider_exceptions import CreateSpiderException


class BaseSpider(Spider):
    name = "base-spider"
    required_keys = []
    id_fields = []
    schema_path = "/app/base_crawler/schemas/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.required_keys == [] or self.id_fields == []:
            raise CreateSpiderException()

    def _parse_input(self, input_):
        if not isinstance(input_, dict):
            try:
                input_ = json.loads(input_)
            except json.JSONDecodeError:
                raise CreateSpiderException("Invalid Input")
        return input_

    def debug_response_file(self, response, **kwargs):
        if os.environ.get("DEBUG_MODE", "true") == "false":
            return None
        file_name_with_extension = kwargs["file_name"]
        file_name, extension = file_name_with_extension.split(".", maxsplit=1)
        path = kwargs.get("path", "/app/tests/files/debug/")
        i = 1
        while os.path.exists(f"{path}{file_name}_{i}.{extension}"):
            i += 1

        with open(f"{path}{file_name}_{i}.{extension}", "wb") as f:
            f.write(response.body)

    def closed(self, reason):
        item_scraped_count = self.crawler.stats.get_value("item_scraped_count")
        elapsed_time_seconds = self.crawler.stats.get_value("elapsed_time_seconds")
        if item_scraped_count is not None and elapsed_time_seconds is not None:
            if elapsed_time_seconds > 0:
                items_scraped_per_second = item_scraped_count / elapsed_time_seconds
                self.crawler.stats.set_value(
                    "items_scraped_per_second", items_scraped_per_second
                )
