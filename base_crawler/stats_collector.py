from scrapy.statscollectors import StatsCollector
from .helper import save_item_stats_to_database
from uuid import uuid4



class MongoStatsCollector(StatsCollector):
    def _persist_stats(self, stats, spider):
        save_item_stats_to_database(
            "stats_collector",
            spider.name,
            {
                "_id": uuid4(),
                "stats": stats,
            },
        )

   