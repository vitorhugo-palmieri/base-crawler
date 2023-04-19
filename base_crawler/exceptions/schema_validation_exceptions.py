import logging

from scrapy.exceptions import DropItem

logger = logging.getLogger("schema exceptions")


class SchemaPipelineException(DropItem):
    def __init__(self, message, item=None):
        message = f"Error in schema pipeline {message}"
        if item is not None:
            message += f" - Error in item {item}"
        super().__init__(message)
        logger.critical(message)
