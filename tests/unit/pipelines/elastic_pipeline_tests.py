# import unittest

# from base_crawler.pipelines.elastic_pipeline import ElasticPipeline
# from base_crawler.exceptions.elastic_exceptions import ElasticNoDateFieldsException
# from tests.spiders.mock_spider_success import MockSpiderSuccess

# class ElasticPipelineTests(unittest.TestCase):

#     def setUp(self):
#         self.pipeline = ElasticPipeline()
#         self.spider = MockSpiderSuccess()

#     def test_get_elastic_index_name_when_has_crawler_on_name(self):
#         crawler_name = "crawler-juris-something"
#         expected_index_name = "juris-something"

#         self.assertEqual(expected_index_name, self.pipeline._get_elastic_index_name(crawler_name))

#     def test_get_elastic_index_name_when_doesnt_have_crawler_on_name(self):
#         crawler_name = "juris-something"
#         expected_index_name = "jurisprudencia"

#         self.assertEqual(expected_index_name, self.pipeline._get_elastic_index_name(crawler_name))

#     def test_elastic_pipeline_should_insert_item_successfully(self):
#         expected_item = {
#             "_id": "testId",
#             "data": {
#                 "testKey": "testValue",
#                 "dataPublicacao": "2022-04-07",
#                 "dataIndexacao": "2022-04-07"
#             },
#             "metadata": {
#                 "source": "1"
#             }
#         }

#         input_item = {
#             "_id": "testId",
#             "data": {
#                 "testKey": "testValue",
#                 "dataPublicacao": "2022-04-07"
#             },
#             "metadata": {
#                 "source": "1"
#             }
#         }

#         actual_item = self.pipeline.process_item(input_item, self.spider)
#         self.assertDictEqual(expected_item, actual_item)

#     def test_elastic_pipeline_should_raise_no_date_field_exception(self):
#         input_item = {
#             "_id": "testId",
#             "data": {
#                 "testKey": "testValue"
#             },
#             "metadata": {
#                 "source": "1"
#             }
#         }
#         with self.assertRaises(ElasticNoDateFieldsException):
#             _ = self.pipeline.process_item(input_item, self.spider)

# if __name__ == "__main__":
#     unittest.main()
