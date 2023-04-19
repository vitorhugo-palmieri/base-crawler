# import unittest

# from base_crawler import helper
# from base_crawler.pipelines.mongo_pipeline import MongoPipeline
# from tests.spiders.mock_spider_success import MockSpiderSuccess
# from tests.test_helper import drop_collection_in_database

# class MongoPipelineTests(unittest.TestCase):

#     def setUp(self):
#         self.pipeline = MongoPipeline()
#         self.spider = MockSpiderSuccess()

#     def tearDown(self):
#         drop_collection_in_database("outputs", self.spider.name)

#     def test_mongo_pipeline_should_process_item_correctly(self):
#         expected_item = {
#             "_id": "testId",
#             "testKey": "testValue"
#         }

#         input_item = {
#             "_id": "testId",
#             "testKey": "testValue"
#         }

#         actual_item = self.pipeline.process_item(input_item, self.spider)
#         found_item = helper.find_item_in_database("outputs", self.spider.name, {"testKey": "testValue"})
#         self.assertDictEqual(expected_item, found_item)
#         self.assertDictEqual(expected_item, actual_item)

# if __name__ == "__main__":
#     unittest.main()
