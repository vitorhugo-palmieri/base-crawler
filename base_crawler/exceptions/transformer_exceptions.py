import logging

from scrapy.exceptions import DropItem

logger = logging.getLogger("transformer pipeline exceptions")


class TransformerPipelineException(DropItem):
    def __init__(self, message):
        super().__init__(message)
        logger.error(
            f"Item dropped. Exception occurred in transformer pipeline {message}"
        )
