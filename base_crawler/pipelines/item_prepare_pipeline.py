from hashlib import md5
from datetime import datetime

from scrapy.exceptions import DropItem

from base_crawler.exceptions.spider_exceptions import OutputException
from base_crawler.helper import save_item_error_to_database
from base_crawler.helper import convert_iso_datetime_to_utc, create_item_id, clean_item


class ItemPreparePipeline:
    def __init__(self):
        self.id_hash = md5()

    def _create_item_id(self, item, id_fields):
        return create_item_id(item, id_fields)

    def _clean_item(self, item):
        return clean_item(item)



    def _add_metadata_to_item(self, item, spider):
        metadata_item = {
            "metadata": {
                "processingDate": convert_iso_datetime_to_utc(str(datetime.now())),
                "spiderName": spider.name,
                "input": spider.input,
                "reprocessed": False,
            }
        }

        item.update(metadata_item)

    def _build_data(self, item):
        item["data"] = {**item}
        for item_key in list(item.keys()):
            if item_key == "data":
                continue
            del item[item_key]

    def _build_item(self, item, **kwargs):
        self._build_data(item)
        self._add_metadata_to_item(item, kwargs.get("spider"))
        item["_id"] = kwargs.get("id_string")
        return item

    def process_item(self, item, spider):
        if not item:
            raise DropItem("Item is Empty")
        self.id_hash = md5()
        for required_key in spider.required_keys:
            if required_key not in item:
                output_exception = OutputException(required_key)
                save_item_error_to_database(spider.name, item, output_exception)
                raise output_exception
        id_string = self._create_item_id(item, spider.id_fields)
        new_item = self._build_item(item.copy(), id_string=id_string, spider=spider)
        item_cleaned = self._clean_item(new_item)
        spider.logger.debug(f"Item prepared - {item_cleaned}")
        return item_cleaned
