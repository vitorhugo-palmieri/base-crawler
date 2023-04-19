import os
import unittest

from base_crawler import helper
from tests import test_helper
from pymongo import MongoClient


class HelperTests(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient(
            "mongo",
            username=os.environ["MONGO_USER"],
            password=os.environ["MONGO_PASS"],
        )
        self.error_database = self.client["errors"]
        self.error_collection = self.error_database["spider_errors"]

    def tearDown(self):
        self.error_collection.drop()
        self.client["spider"]["items"].drop()

    def test_save_item_error_correctly(self):
        error_item = {"key": "value"}

        error = "item with error"

        expected_saved_error = {
            "_id": "8b5f63f07b5853597c56cf396c29d75c",
            "data": {
                "key": "value",
            },
            "error": "item with error",
        }

        self.assertIsNone(
            helper.save_item_error_to_database("spider", error_item, error)
        )
        found_error = self.error_collection.find_one({"data": {"key": "value"}})
        self.assertDictEqual(expected_saved_error, found_error)

    def test_find_item_in_database_return_item(self):
        error_item = {"key": "value"}

        error = "item with error"

        expected_error = {
            "_id": "8b5f63f07b5853597c56cf396c29d75c",
            "data": {"key": "value"},
            "error": "item with error",
        }

        self.assertIsNone(
            helper.save_item_error_to_database("spider", error_item, error)
        )
        found_error = helper.find_item_in_database(
            "errors", "spider_errors", {"data": {"key": "value"}}
        )
        self.assertDictEqual(expected_error, found_error)

    def test_save_item_to_database(self):
        item_to_insert = {"_id": 1, "key": "value"}

        helper.save_item_to_database("spider", "items", item_to_insert)
        database = self.client["spider"]
        collection = database["items"]
        found_item = collection.find_one({"_id": 1})
        self.assertDictEqual(item_to_insert, found_item)

    def test_load_json_successfully(self):
        file_binary = test_helper.read_test_file("test_file.json")
        json_obj = helper.load_json(file_binary)
        self.assertIsNotNone(json_obj)

    def test_is_json_file_return_true(self):
        file_binary = test_helper.read_test_file("test_file.json")
        self.assertTrue(helper.is_valid_json(file_binary))

    def test_is_json_file_return_false(self):
        file_binary = test_helper.read_test_file("test_file.txt")
        self.assertFalse(helper.is_valid_json(file_binary))

    def test_parse_date_without_timezone_successfully(self):
        date_without_timezone = "2021-01-01 00:00:00"
        expected_date = "2021-01-01T03:00:00+00:00"
        self.assertEqual(
            expected_date, helper.convert_iso_datetime_to_utc(date_without_timezone)
        )

    def test_parse_date_with_timezone_successfully(self):
        date_with_timezone = "2021-01-01T00:00:00-0300"
        expected_date = "2021-01-01T03:00:00+00:00"
        self.assertEqual(
            expected_date, helper.convert_iso_datetime_to_utc(date_with_timezone)
        )

    def test_parse_date_without_hour_successfully(self):
        date_with_timezone = "2021-01-01"
        expected_date = "2021-01-01T03:00:00+00:00"
        self.assertEqual(
            expected_date, helper.convert_iso_datetime_to_utc(date_with_timezone)
        )

    def test_validate_date_format_successfully(self):
        date_string = "2021-01-01"
        self.assertTrue(helper.validate_date_format(date_string))

    def test_validate_date_format_return_false(self):
        date_string = "01/01/2021"
        self.assertFalse(helper.validate_date_format(date_string))

    def test_convert_date_from_iso_to_br_successfully(self):
        date_string = "2021-01-01"
        expected_date = "01/01/2021"
        self.assertEqual(expected_date, helper.convert_date_from_iso_to_br(date_string))

    def test_convert_date_from_iso_to_br_return_none(self):
        date_string = "01/01/01"
        self.assertIsNone(helper.convert_date_from_iso_to_br(date_string))

    def test_convert_date_from_br_to_iso_successfully(self):
        date_string = "01/01/2021"
        expected_date = "2021-01-01"
        self.assertEqual(expected_date, helper.convert_date_from_br_to_iso(date_string))

    def test_convert_date_from_br_to_iso_return_none(self):
        date_string = "2021-01-01"
        self.assertIsNone(helper.convert_date_from_br_to_iso(date_string))

    def test_remove_non_digit(self):
        first_string = "3h4jk3hjkhjkferwdfu789uj3453nm,.,mnm432,.4hiou89"
        expected_first_string = "3437893453432489"
        second_string = ""
        expected_second_string = ""
        self.assertEqual(expected_first_string, helper.remove_non_digit(first_string))
        self.assertEqual(expected_second_string, helper.remove_non_digit(second_string))

    def test_body_to_soup_return_valid_object(self):
        html_file = test_helper.read_test_file("test_file.html")
        self.assertIsNotNone(helper.body_to_soup(html_file))

    def test_body_to_soup_return_none(self):
        self.assertIsNone(helper.body_to_soup(None))

    def test_find_element_by_dict_key_in_array_return_element(self):
        input_array = [{"data": {"key": "value1"}}, {"data": {"key": "value2"}}]

        expected_element = {"data": {"key": "value2"}}

        found_element = helper.find_element_by_dict_key_in_array(
            input_array, {"data.key": "value2"}
        )
        self.assertDictEqual(expected_element, found_element)

    def test_find_element_by_dict_key_in_array_return_none_when_conditions_are_false(
        self,
    ):
        input_array = ["1", "2", "3"]

        found_element = helper.find_element_by_dict_key_in_array(
            input_array, {"key": "value"}
        )
        self.assertIsNone(found_element)

    def test_find_element_by_dict_key_in_array_return_none_when_lookup_not_found(self):
        input_array = [{"data": {"key": "value1"}}, {"data": {"key": "value2"}}]

        found_element = helper.find_element_by_dict_key_in_array(
            input_array, {"data.key": "value3"}
        )
        self.assertIsNone(found_element)

    def test_create_file_name_should_create_correctly(self):

        file_parameters = {
            "tribunal": "TJSP",
            "dataPublicacao": "2021-01-01",
            "numeroDecisao": "23743824789",
            "classeProcessual": "Agravo de Instrumento",
        }

        bucket_parameters = {
            "tribunal": "TJSP",
            "dataPublicacao": "2021-01-01",
            "extensao": "pdf",
        }

        expected_file_name = "TJSP/2021-01-01/e0507fbdac648f1328efede77d8a8104.pdf"

        self.assertEqual(
            expected_file_name,
            helper.create_file_name(file_parameters, bucket_parameters),
        )


if __name__ == "__main__":
    unittest.main()
