import unittest
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from base_crawler import helper
from tests import test_helper

logger = logging.getLogger("integration tests")


class IntegrationTestFixture(unittest.TestCase):
    def setup_crawler(self, settings=get_project_settings()):
        self.process = CrawlerProcess(settings=settings)

    def tear_down_outputs_database(self, spider_name):
        test_helper.drop_collection_in_database("STG_outputs", spider_name)

    def tear_down_transformed_outputs_database(self, spider_name):
        test_helper.drop_collection_in_database("STK_inputs", spider_name)

    def tear_down_errors_database(self, spider_name):
        test_helper.drop_collection_in_database("errors", f"{spider_name}_errors")

    def _assert_item_found(self, spider_name, expected_item, lookup):
        found_item = helper.find_item_in_database("STK_inputs", spider_name, lookup)
        self.assertIsNotNone(found_item)
        self.assertDictEqual(expected_item, found_item)

    def _assert_multiple_items_found(self, spider_name, expected_items=[], lookups=[]):
        """
        This method asserts for multiple items collected by the spider.
        Based on a lookup, it obtains a record from the database and compares it to the corresponding expected item.
        If the item is not found in the database, the assertion will fail, so this method asserts if all the expected items are in fact in the database.
        """
        if len(expected_items) != len(lookups):
            logger.error("Expected items and lookups size not compatible")
            raise Exception("Expected items and lookups size not compatible")

        for i in range(0, len(lookups)):
            found_item_in_database = helper.find_item_in_database(
                "STK_inputs", spider_name, lookups[i]
            )
            found_item_in_expected = test_helper.find_element_by_dict_key_in_array(
                expected_items, lookups[i]
            )
            self.assertDictEqual(found_item_in_expected, found_item_in_database)

    def _assert_item_not_found(self, spider_name, lookup):
        found_item = helper.find_item_in_database("STK_inputs", spider_name, lookup)
        self.assertIsNone(found_item)

    def _assert_pipeline_error(self, spider_name, stats, lookup):
        self.assertIsNone(
            helper.find_item_in_database("STK_inputs", spider_name, lookup)
        )
        self.assertEqual(1, stats.get_value("item_dropped_count"))

    def _assert_spider_finish_reason(self, stats, finish_reason):
        self.assertEqual(finish_reason, stats.get_value("finish_reason"))
