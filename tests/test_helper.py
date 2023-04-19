"""
The purpose of this module is to provide functions to be used in tests.
You may use it in other places, but some folder paths are mapped to test folders inside the container, so it's highly encouraged to use the functions only in tests.
"""

import os
import json

from pymongo import MongoClient
from base_crawler import helper


def drop_collection_in_database(database_name, collection_name):
    with MongoClient(
        "mongo",
        username=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"],
    ) as client:
        database = client[database_name]
        collection = database[collection_name]
        collection.drop()


def read_test_file(file_name):
    """
    This function reads a test file as bytes.
    This is useful for testing parser functions that parse a response body, because the response.body attribute in spider is always a bytes object.
    """
    with open(f"/app/tests/files/tests_files/{file_name}", "rb") as f:
        return f.read()


def read_test_file_as_text(file_name):
    """
    This function reads a test file as string
    """
    with open(f"/app/tests/files/tests_files/{file_name}", "r") as f:
        return f.read()


def read_test_file_as_json(file_name):
    """
    This function reads a json file inside the tests_files folder and returns a dictionary.

    Important
    ---------
    You must not write .json in the file name passed as argument
    """
    with open(f"/app/tests/files/tests_files/{file_name}.json", "rb") as f:
        return helper.load_json(f.read())


def save_test_file_as_json(file_name, json_obj):
    """
    This function saves a dictionary passed as argument to a json file.

    Important
    ---------
    You must not write .json in the file name passed as argument
    """
    with open(f"/app/tests/files/tests_files/{file_name}.json", "w") as f:
        json.dump(json_obj, f)


def find_element_by_dict_key_in_array(array, lookup):
    """
    This function is used by the spider integration tests to find an item in an array by a lookup.

    The lookup could be in a dict format or in the mongo notation format.

    Examples:

    {"data":{"key":"value"}} or {"data.key":"value"}
    """
    conditions = [
        not all(type(element) is dict for element in array),
        type(lookup) is not dict,
        len(lookup) != 1,
    ]
    if any(conditions):
        return None

    lookup_key = list(lookup.keys())[0].split(".")[-1]
    lookup_value = list(lookup.values())[0]

    if lookup_key == "_id":
        return _find_element_by_id(array, lookup_value)
    else:
        return _find_element_by_key(array, lookup_key, lookup_value)


def _find_element_by_id(array, lookup_value):
    for element in array:
        if element["_id"] == lookup_value:
            return element
    return None


def _find_element_by_key(array, lookup_key, lookup_value):
    for element in array:
        if element["data"].get(lookup_key) == lookup_value:
            return element
    return None
