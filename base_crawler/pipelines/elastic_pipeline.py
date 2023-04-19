import os
from pickle import NONE

from elasticsearch import Elasticsearch

from base_crawler.helper import save_item_error_to_database
from base_crawler.exceptions import elastic_exceptions


def _get_elastic_search_host():
    elastic_host = os.environ.get("ELASTIC_HOST")
    if not elastic_host:
        return "elasticsearch"
    return elastic_host


def _get_elastic_authentication_parameters():
    elastic_user = os.environ.get("ELASTIC_USER")
    elastic_pass = os.environ.get("ELASTIC_PASSWORD")

    if not elastic_user or not elastic_pass:
        return None

    return (elastic_user, elastic_pass)


def _get_elastic_env_variable(variable_name, default_value):
    elastic_variable = os.environ.get(variable_name)

    if not elastic_variable:
        return default_value

    return elastic_variable


class ElasticPipeline:
    def __init__(self):
        try:
            self.elastic_connection = Elasticsearch(
                hosts=_get_elastic_search_host(),
                http_auth=_get_elastic_authentication_parameters(),
                scheme=_get_elastic_env_variable("ELASTIC_SCHEME", "https"),
                port=int(_get_elastic_env_variable("ELASTIC_PORT", 9200)),
                use_ssl=False,
                verify_certs=False,
            )
        except:
            raise elastic_exceptions.ElasticConnectionException()

    def _delete_unecessary_keys(self, item):
        del item["_id"]
        del item["data"]
        del item["metadata"]

    def _add_data_and_metadata_to_doc(self, item):
        """
        This method transforms the item to the correct format expected by elasticsearch
        """
        item["doc"] = {}
        item["doc"]["id"] = item["_id"]
        item["doc"]["data"] = item["data"]
        item["doc"]["metadata"] = item["metadata"]

    def _create_elastic_object(self, item):
        item_elastic = item.copy()

        item_elastic["doc_as_upsert"] = True
        self._add_data_and_metadata_to_doc(item_elastic)
        self._delete_unecessary_keys(item_elastic)
        return item_elastic

    def _get_elastic_index_name(self, crawler_name):
        if "crawler-" not in crawler_name:
            return "jurisprudencia"
        splited_name = crawler_name.split("-")

        return "-".join(splited_name[1:])

    def process_item(self, item, spider):
        self.spider_name = spider.name
        item_elastic = self._create_elastic_object(item)
        index_name = self._get_elastic_index_name(spider.name)

        self.elastic_connection.update(
            index_name, item_elastic["doc"]["id"], item_elastic, refresh=True
        )
        spider.logger.info(
            f"Spider name: {spider.name}. Inserted item {item_elastic} in elastic"
        )
        return item
