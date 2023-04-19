import os
from pymongo import MongoClient
from base_crawler.exceptions.mongo_exceptions import MongoPipelineException
from base_crawler.helper import _get_mongo_port_from_env, _get_mongo_url_from_env
import re


class MongoPipeline:
    database = os.environ["MONGO_DATABASE"]
    seen_ids = set()

    def open_spider(self, spider):
        self.counter = 0
        self.mongo_client = MongoClient(
            _get_mongo_url_from_env(),
            username=os.environ["MONGO_USER"],
            password=os.environ["MONGO_PASSWORD"],
            port=_get_mongo_port_from_env(),
        )

    def get_item_year(self,item):
        year = item.get('metadata').get('input').get('date','')[:4]
        if year != '':
            return f"-{year}"
        else:
            return year

    def process_item(self, item, spider):
        year = self.get_item_year(item)
        court = re.sub(r'-','_',re.sub('crawler-juris-','',spider.name))
        court = re.sub(r'_d_1','',court)
        database = self.mongo_client[f"{self.database}_{court}"]
        collection = database[f"{re.sub('-d-1','',spider.name)}{year}"]
        try:
            collection.update_one({"_id": item["_id"]}, {"$set": item}, upsert=True)
            return item
        except Exception as e:
            spider.logger.error(str(e))
            raise MongoPipelineException(str(e))


    def close_spider(self, spider):
        spider.logger.info("==== seen_ids {}".format(len(self.seen_ids)))
        self.mongo_client.close()
