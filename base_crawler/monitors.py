from spidermon import Monitor, monitors
from spidermon.core.suites import MonitorSuite
from spidermon.contrib.scrapy.monitors import ErrorCountMonitor, FinishReasonMonitor
from spidermon.core.actions import Action
from math import ceil
from spidermon.contrib.actions.discord import SendDiscordMessage
from base_crawler.helper import _get_mongo_port_from_env, _get_mongo_url_from_env
import os
from pymongo import MongoClient



class CustomSendDiscordMessage(SendDiscordMessage):
    def get_message(self):
        stats = self.data.stats
        n_scraped_items = stats.get("item_scraped_count", 0)
        n_expected_scraped_items = stats.get("expected_num_items")
        failures = len(self.result.failures)
        emoji = "❌" if failures > 0 else "✅"
        query = f"{{'timestamp':{{$gte: ISODate('{stats['start_time']}'),$lte:ISODate('{stats['finish_time']}')}}}}"
        message = "\n".join(
            [
                f"**{self.data.spider.name}**:",
                f"- Finished reason: {stats['finish_reason']}",
                f"- Input: {stats['input']}",
                f"- Start time: *{stats['start_time']}*",
                f"- Finish time: *{stats['finish_time']}*",
                f"- Mongo query to find execution in logs: *{query}*",
                f"- Documents scraped: *{n_scraped_items}*",
                f"- Expected documents scraped: *{n_expected_scraped_items}*"
                if n_expected_scraped_items is not None
                else "No items in Court",
                f"  {emoji} {failures} failures {emoji}",
            ]
        )
        return message


class ItemCountMonitor(Monitor):
    # def save_mongodb(self):
    #     stats = self.data.stats
    #     total_results = stats.get("total_results")
    #     with MongoClient(_get_mongo_url_from_env(),
    #         username=os.environ["MONGO_USER"],
    #         password=os.environ["MONGO_PASSWORD"],
    #         port=_get_mongo_port_from_env(),
    #     ) as client:
    #         database = client['crawlers_inputs']
    #         collection = database[self.data.spider.name]
    #         collection.update_one({"_id":stats["input"]},{"$set":{"esperado":total_results}},upsert=True)
 

    def test_expected_items_scraped_is_equal_items_scraped(self):
        #self.save_mongodb()
        expected_num_items = self.data.stats.get("expected_num_items")
        if expected_num_items is not None or expected_num_items != 0:
            items_scraped = self.data.stats.get("item_scraped_count", 0)
            self.assertTrue(items_scraped >= ceil(expected_num_items * 0.9))



class ItemDownloaderCountMonitor(Monitor):
    def test_expected_items_downloaded_is_equal_expected(self):
        expected_items_downloaded = self.data.stats.get("expected_items_downloaded")
        if expected_items_downloaded is not None or expected_items_downloaded != 0:
            items_downloaded = self.data.stats.get("download_items_count", 0)
            self.assertTrue(items_downloaded >= ceil(expected_items_downloaded * 0.9))


class SpiderCloseMonitorSuite(MonitorSuite):
    monitors = [
        ItemCountMonitor,
        FinishReasonMonitor,
    ]
    monitors_failed_actions = [CustomSendDiscordMessage]


class DownloaderCloseMonitorSuite(MonitorSuite):
    monitors = [
        ItemDownloaderCountMonitor,
        FinishReasonMonitor,
    ]
    monitors_failed_actions = [CustomSendDiscordMessage]
