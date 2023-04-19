import os
import re
import json
from hashlib import md5
from datetime import datetime
import pika
from dateutil.tz import UTC
from dateutil.tz import gettz
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dateutil.parser import parse as parse_date
from base_crawler.exceptions.item_clean_exceptions import FieldNotInItemException


BASE_TO_ANALYSE = os.environ.get("BASE_TO_ANALYSE", "STK_inputs")

_KEYS_TO_IGNORE = ["_id", "metadata", "id_com_cdacordao"]
year_regex=re.compile(r'[0-9][0-9][0-9][0-9]')

_KEYS_NOT_UPPER = [
    "url",
    "idArquivo",
    "extensao",
    "nomeArquivo",
    "inteiroTeorTexto",
    "ementa",
    "cdAcordao",
]


def _get_mongo_port_from_env():
    mongo_port = os.environ.get("MONGO_PORT")
    if not mongo_port:
        return 27017
    return int(mongo_port)


def _get_mongo_url_from_env():
    mongo_url = os.environ.get("MONGO_HOST")
    if not mongo_url:
        return "mongo"
    return mongo_url

def get_item_year(input):
    year = input.get('date','')[:4]
    if year != '':
        return f"-{year}"
    else:
        return year

def _find_item_existing_in_database(crawler_name, _input):
    court = re.sub('-','_',re.sub('crawler-juris-','',crawler_name))
    court = re.sub(r'_d_1','',court).lower()
    crawler_name = re.sub(r'-d-1','',crawler_name)
    year = get_item_year(_input)
    with MongoClient(
        _get_mongo_url_from_env(),
        username=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"],
        port=_get_mongo_port_from_env(),
    ) as client:
        database = client[f'{BASE_TO_ANALYSE}_{court}']
        collection = database[f'{crawler_name}{year}']
        cursor = collection.find(
            {"metadata.input": _input},
            {"_id": 1},
            no_cursor_timeout=True,
        )
        items = [item.get("_id") for item in cursor]

        cursor.close()

        return items


def get_decisions_to_ignore(crawler_name, spider_input):
    if spider_input.get("recrawl"):
        del spider_input["recrawl"]
        decisions = _find_item_existing_in_database(
            crawler_name,
            spider_input,
        )
        return decisions
    return []


def find_item_in_database(database_name, collection, lookup):
    with MongoClient(
        _get_mongo_url_from_env(),
        username=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"],
        port=_get_mongo_port_from_env(),
    ) as client:
        database = client[database_name]
        collection = database[collection]
        found_item = collection.find_one(lookup)
        return found_item


def save_item_to_database(database_name, collection, item,court_name):
    year=get_year_of_document(item)
    court = re.sub(r'-','_',re.sub('crawler-juris-','',court_name))
    court = re.sub(r'd-1','',court).lower()
    collection = collection.lower()
    with MongoClient(
        _get_mongo_url_from_env(),
        username=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"], 
        port=_get_mongo_port_from_env(),
    ) as client:
        database = client[f"{database_name}_{court}"]
        collection = database[f'{collection}-{year}']
        collection.update_one({"_id": item["_id"]}, {"$set": item}, upsert=True)

def get_year_of_document(item):
    data_document = item.get('data').get('dataPublicacao',item.get('data').get('dataJulgamento',''))
    year = re.findall(year_regex,item.get('metadata').get('input').get('date',data_document))
    if len(year) == 0:
        return 'NO_DATE'
    else:
        return year[0]
    
def save_item_stats_to_database(database_name, collection, item):
    with MongoClient(
        _get_mongo_url_from_env(),
        username=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"],
        port=_get_mongo_port_from_env(),
    ) as client:
        database = client[database_name]
        collection = database[collection]
        collection.update_one({"_id": item["_id"]}, {"$set": item}, upsert=True)

    

def save_item_error_to_database(spider_name, item, error):
    with MongoClient(
        _get_mongo_url_from_env(),
        username=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"],
        port=_get_mongo_port_from_env(),
    ) as client:
        error_database = client["errors"]
        item_clean_pipeline_error_collection = error_database[f"{spider_name}_errors"]
        id_hash = md5()
        string_to_encode = str(item) + str(error)
        id_hash.update(string_to_encode.encode())
        error_object = {"_id": id_hash.hexdigest(), "data": item, "error": str(error)}
        item_clean_pipeline_error_collection.insert_one(error_object)



def load_json(json_body):
    try:
        json_obj = json.loads(json_body.decode())
        return json_obj
    except:
        return None


def is_valid_json(body):
    try:
        _ = json.loads(body.decode())
        return True
    except:
        return False


def save_json_to_file(file_path, json_obj):
    with open(file_path, "w") as f:
        json.dump(json_obj, f)


def convert_iso_datetime_to_utc(date_string):
    """
    This function converts a datetime in America/Sao_Paulo timezone to UTC timezone
    """
    parsed_date = parse_date(date_string, yearfirst=True)
    date_with_timezone = parsed_date
    if parsed_date.tzinfo is None:
        date_with_timezone = parsed_date.replace(tzinfo=gettz("America/Sao_Paulo"))
    return date_with_timezone.astimezone(UTC).isoformat(timespec="seconds")


def convert_date_from_iso_to_br(date_string):
    if not validate_date_format(date_string):
        return None
    return datetime.strftime(datetime.strptime(date_string, "%Y-%m-%d"), "%d/%m/%Y")


def convert_date_from_br_to_iso(date_string):
    if not validate_date_format(date_string, "%d/%m/%Y"):
        return None
    return datetime.strftime(datetime.strptime(date_string, "%d/%m/%Y"), "%Y-%m-%d")


def validate_date_format(date_string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except:
        return False


def remove_non_digit(string):
    return re.sub(r"\D", "", string)


def body_to_soup(body, parser="html.parser", encoding="utf-8"):
    try:
        return BeautifulSoup(body, parser, from_encoding=encoding)
    except Exception:
        return None


def find_element_by_dict_key_in_array(array, lookup):
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
    return None


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


def get_rabbit_credentials():
    rabbit_user = os.environ.get("RABBIT_USER")
    rabbit_pass = os.environ.get("RABBIT_PASS")
    if not rabbit_user or not rabbit_pass:
        return pika.credentials.PlainCredentials("guest", "guest")
    return pika.credentials.PlainCredentials(rabbit_user, rabbit_pass)


def get_rabbit_host():
    rabbit_host = os.environ.get("RABBIT_HOST")
    if not rabbit_host:
        return "rabbitmq"
    return rabbit_host


def create_file_name(id_parameters: dict, bucket_parameters: dict):
    """
    This function creates a file name that should be the file name in a bucket.

    Parameters
    ----------
        id_parameters: dictionary with keys that will be used to form the md5 hash id for this file. The keys will be sorted.
        bucket_parameters: dictionary with tribunal, dataPublicacao and extensao keys. This information will be used to form the file_name in the bucket with the correct folder structure.
    """
    id_parameters_keys = list(id_parameters.keys())
    id_parameters_keys.sort()
    file_id_hash = md5()
    for id_parameter_key in id_parameters_keys:
        file_id_hash.update(id_parameters[id_parameter_key].encode())

    file_id = file_id_hash.hexdigest()

    file_court = bucket_parameters["tribunal"]
    file_publish_date = bucket_parameters["dataPublicacao"]
    file_extension = bucket_parameters["extensao"]

    return f"{file_court}/{file_publish_date}/{file_id}.{file_extension}"


def create_item_id(item, id_fields):
    """
    This method receives the id fields declared in the crawler and creates an
    md5 hash of these fields.

    Important
    ---------
    The md5 hash is created using the fields in the order declared. This
    information is useful if an id recovery process should be required.
    """
    id_hash = md5()

    for field in id_fields:
        if type(field) is str:
            if field not in item:
                raise FieldNotInItemException(field, item)
            if type(item[field]) is str:
                id_hash.update(item[field].encode())
            elif type(item[field]) is int or type(item[field] is float):
                id_hash.update(str(item[field]).encode())
        if type(field) is dict:
            field_key = list(field.keys())[0]
            field_value = list(field.values())[0]
            if field_key not in item:
                raise FieldNotInItemException(field_key, item)
            create_item_id(item[field_key], [field_value])
    else:
        return id_hash.hexdigest()


def _clean_list(item):
    cleaned_list = []
    for element in item:
        if element is None:
            continue
        if type(element) is str:
            cleaned_list.append(_clean_string(element))
            continue
        elif type(element) is list:
            if len(element) == 0:
                continue
            cleaned_list.append(_clean_list(element))
            continue
        elif type(element) is dict:
            cleaned_list.append(clean_item(element))
            continue
        cleaned_list.append(element)
    return cleaned_list


def _clean_string(item):
    return item.upper().strip()


def clean_item(item):
    """
    This method recursively cleans an item. It traverses the item until a string is found, and the string is converted to uppercase and stripped.
    This method currently does not set a limit for recursion level, so be careful with deep objects.
    None values are discarded from the item.
    """
    if type(item) is dict:
        item_keys = list(item.keys())
        for item_key in item_keys:
            if any(key_to_ignore in item_key for key_to_ignore in _KEYS_TO_IGNORE):
                continue
            dict_value = item[item_key]
            if dict_value is None:
                del item[item_key]
                continue
            if type(dict_value) is list:
                if len(dict_value) == 0:
                    del item[item_key]
                    continue
                item[item_key] = _clean_list(dict_value)
            elif type(dict_value) is dict:
                item[item_key] = clean_item(dict_value)
            elif type(dict_value) is str:
                cleaned_string = _clean_string(dict_value)
                if cleaned_string == "":
                    del item[item_key]
                    continue
                if any(key_to_ignore in item_key for key_to_ignore in _KEYS_NOT_UPPER):
                    continue
                item[item_key] = cleaned_string
        return item
