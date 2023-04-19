# import unittest

# from base_crawler.pipelines.rabbit_pipeline import RabbitPipeline
# from tests.spiders.mock_spider_success import MockSpiderSuccess


# class RabbitPipelineTests(unittest.TestCase):

#     def setUp(self):
#         self.pipeline = RabbitPipeline()
#         self.spider = MockSpiderSuccess()

#     def test_rabbit_pipeline_should_publish_item_successfully(self):
#         expected_item = {
#             "_id": "testId",
#             "testKey": "testValue"
#         }

#         input_item = {
#             "_id": "testId",
#             "testKey": "testValue"
#         }

#         actual_item = self.pipeline.process_item(input_item, self.spider)
#         self.assertDictEqual(expected_item, actual_item)
