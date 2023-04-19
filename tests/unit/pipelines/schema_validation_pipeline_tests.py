# import unittest

# from jsonschema import ValidationError
# from scrapy.exceptions import DropItem

# from tests.test_helper import drop_collection_in_database
# from base_crawler.pipelines.schema_validation_pipeline import SchemaValidationPipeline
# from base_crawler.exceptions.spider_exceptions import InvalidSpiderAttributesException
# from tests.spiders.mock_spider_success import MockSpiderSuccess

# class SchemaValidationPipelineTests(unittest.TestCase):

#     def setUp(self):
#         self.spider = MockSpiderSuccess()
#         self.pipeline = SchemaValidationPipeline(self.spider.schema_name, self.spider, schema_path="/app/tests/schemas/")

#     def tearDown(self):
#         self.spider = MockSpiderSuccess()
#         drop_collection_in_database("errors", f"{self.spider.name}_errors")

#     def test_schema_validation_pipeline_process_item_successfully(self):
#         expected_item = {
#             "_id": "c4ca4238a0b923820dcc509a6f75849b",
#             "data": {
#                 "idField": 1,
#                 "testKey": "testValue"
#             },
#             "metadata": {
#                 "spiderName": self.spider.name,
#                 "processingDate": "2021-01-01T03:00:00+00:00"
#             }
#         }

#         input_item = {
#             "_id": "c4ca4238a0b923820dcc509a6f75849b",
#             "data": {
#                 "idField": 1,
#                 "testKey": "testValue"
#             },
#             "metadata": {
#                 "spiderName": self.spider.name,
#                 "processingDate": "2021-01-01T03:00:00+00:00"
#             }
#         }

#         actual_item = self.pipeline.process_item(input_item, self.spider.schema_name)
#         self.assertDictEqual(expected_item, actual_item)

#     def test_schema_validation_pipeline_open_schema_file_raise_file_exception(self):
#         with self.assertRaises(DropItem):
#             _ = self.pipeline._open_schema_file('spider-not-found-name')

#     def test_schema_validation_pipeline_process_item_raise_drop_item_exception(self):
#         input_item = {
#             "idField": 1,
#             "testKey": "testValue",
#             "invalidKey": "invalid"
#         }

#         with self.assertRaises(DropItem):
#             _ = self.pipeline.process_item(input_item, self.spider.schema_name)


# if __name__ == "__main__":
#     unittest.main()
