import logging

from scrapy.exceptions import DropItem

logger = logging.getLogger("elastic exceptions")


class ElasticConnectionException(DropItem):
    def __init__(self):
        super().__init__()
        logger.error(f"Item dropped. Exception ocurred in connection to elastic")


class ElasticNoDateFieldsException(DropItem):
    def __init__(self):
        super().__init__()
        logger.error(
            f"Item dropped. No dataPublicacao or dataJulgamento fields in data"
        )
