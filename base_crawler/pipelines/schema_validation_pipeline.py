import json

from jsonschema import validate as validate_schema
from jsonschema import ValidationError

from base_crawler.helper import save_item_error_to_database
from base_crawler.exceptions.schema_validation_exceptions import SchemaPipelineException


class SchemaValidationPipeline:
    def __init__(self, schema_name, spider, schema_path="/app/base_crawler/schemas/"):
        self.schema_path = schema_path
        self.schema = self._open_schema_file(schema_name)
        self.spider = spider

    @classmethod
    def from_crawler(cls, crawler):
        schema_name = "common-bot-schema"
        if hasattr(crawler.spider, "schema_name"):
            schema_name = crawler.spider.schema_name
        if hasattr(crawler.spider, "schema_path"):
            return cls(
                schema_name=schema_name,
                spider=crawler.spider,
                schema_path=crawler.spider.schema_path,
            )
        return cls(schema_name=schema_name, spider=crawler.spider)

    def _open_schema_file(self, schema_name):
        try:
            with open(f"{self.schema_path}{schema_name}.json", "r") as schema_file:
                return json.load(schema_file)
        except FileNotFoundError:
            raise SchemaPipelineException(
                f"File {self.schema_path}{schema_name}.json not found"
            )

    def process_item(self, item, spider):
        try:
            validate_schema(instance=item, schema=self.schema)
            self.spider.logger.debug(f"Schema validated successfully - {item}")
        except ValidationError as e:
            self.spider.logger.critical(f"Validation error {str(e)}")
            save_item_error_to_database(
                self.spider.name, item, f"Validation error {str(e)}"
            )
            raise SchemaPipelineException(f"Invalid schema for item", item)
        return item
