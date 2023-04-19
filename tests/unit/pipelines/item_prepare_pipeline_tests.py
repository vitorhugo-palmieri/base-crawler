# import os
# import unittest
# from pymongo import MongoClient
# from time import sleep

# from freezegun import freeze_time
# from scrapy.exceptions import DropItem

# from base_crawler import helper
# from base_crawler.pipelines.item_prepare_pipeline import ItemPreparePipeline
# from base_crawler.exceptions.spider_exceptions import OutputException
# from tests.spiders.mock_spider_success import MockSpiderSuccess
# from tests.test_helper import drop_collection_in_database


# class ItemPreparePipelineTests(unittest.TestCase):

#     def setUp(self):
#         self.pipeline = ItemPreparePipeline()
#         self.spider = MockSpiderSuccess()
#         self.database_name = "errors"
#         self.collection_name = f"{self.spider.name}_errors"
#         self.maxDiff = None

#     def tearDown(self):
#         drop_collection_in_database(self.database_name, self.collection_name)

#     @freeze_time("2021-01-01 00:00:00")
#     def test_item_prepare_pipeline_should_process_item_correctly(self):
#         expected_item = {
#             "_id": "cda160cc7c895bfcba6c9abc3c123747",
#             "data": {
#                 "testKey": "TESTVALUE",
#             },
#             "metadata": {
#                 "spiderName": "mock-spider-success",
#                 "processingDate": "2021-01-01T03:00:00+00:00",
#                 "input": {
#                     "a": "b"
#                 }
#             }
#         }

#         input_item = {
#             "testKey": "testValue"
#         }

#         actual_item = self.pipeline.process_item(input_item, self.spider)
#         self.assertDictEqual(expected_item, actual_item)

#     def test_item_prepare_pipeline_should_raise_required_key_exception(self):
#         input_item = {
#             "otherKey": "otherValue"
#         }

#         expected_error = {
#             "_id": "2556a53b267d9ea747838ad18d2c2114",
#             "data": {
#                 "otherKey": "otherValue"
#             },
#             "error": "Required key testKey not in item"
#         }

#         with self.assertRaises(OutputException):
#             self.pipeline.process_item(input_item, self.spider)

#         found_error = helper.find_item_in_database(
#             self.database_name, self.collection_name, {"data": {"otherKey": "otherValue"}})
#         self.assertDictEqual(expected_error, found_error)

#     def test_item_prepare_pipeline_should_create_id_successfully(self):
#         expected_id = "bbce045b595cde4759c789c1fd662d69"

#         input_item = {
#             "testKey": "testValue",
#             "objectKey": {
#                 "objectKeyId": 2,
#                 "valueInKey": {
#                     "keyInside": 5.0
#                 }
#             }
#         }

#         actual_id = self.pipeline._create_item_id(input_item, ["testKey", {
#                                                   "objectKey": "objectKeyId"}, {"objectKey": {"valueInKey": "keyInside"}}])
#         self.assertEqual(expected_id, actual_id)

#     def test_item_prepare_pipeline_should_raise_key_error(self):
#         input_item = {
#             "testKey": "testValue",
#             "objectKey": {
#                 "objectKeyId": 2,
#                 "valueInKey": {
#                     "keyInside": 5.0
#                 }
#             }
#         }

#         with self.assertRaises(DropItem):
#             _ = self.pipeline._create_item_id(
#                 input_item, ["testKey", {"keyDoesntExist": "objectKeyId"}])

#     def test_item_prepare_pipeline_should_prepare_item_successfully(self):
#         item_to_prepare = {
#             "stringKey": "       stringValue      ",
#             "dictKey": {
#                 "dictNestedKey1": {
#                     "numberKey": 1,
#                     "listKey": [
#                         "string1",
#                         "string2",
#                         "      string 3\n"
#                     ]
#                 },
#                 "noneValue": None,
#                 "listKeyNested": [
#                     {
#                         "nestedObject1": {
#                             "stringKey": "stringValue     \n",
#                             "stringKey2": "\n\n\nstringValue\n\n\n      "
#                         }
#                     },
#                     {
#                         "nestedObject2": {
#                             "numberKey": 1.0,
#                             "numberKey2": 2,
#                             "emptyList": []
#                         }
#                     }
#                 ]
#             },
#             "emptyList": [],
#             "emptyString": ""
#         }

#         expected_item_prepared = {
#             "stringKey": "STRINGVALUE",
#             "dictKey": {
#                 "dictNestedKey1": {
#                     "numberKey": 1,
#                     "listKey": [
#                         "STRING1",
#                         "STRING2",
#                         "STRING 3"
#                     ]
#                 },
#                 "listKeyNested": [
#                     {
#                         "nestedObject1": {
#                             "stringKey": "STRINGVALUE",
#                             "stringKey2": "STRINGVALUE"
#                         },
#                     },
#                     {
#                         "nestedObject2": {
#                             "numberKey": 1.0,
#                             "numberKey2": 2
#                         }
#                     }
#                 ]
#             }
#         }

#         item_prepared = self.pipeline._clean_item(item_to_prepare)
#         self.assertDictEqual(expected_item_prepared, item_prepared)


# if __name__ == "__main__":
#     unittest.main()
