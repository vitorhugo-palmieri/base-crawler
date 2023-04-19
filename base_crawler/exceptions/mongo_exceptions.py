import logging

from scrapy.exceptions import DropItem

logger = logging.getLogger("mongo exceptions")


class MongoPipelineException(DropItem):
    def __init__(self, message):
        super().__init__(message)
        logger.error(f"Item dropped. Exception occurred in mongo {message}")
