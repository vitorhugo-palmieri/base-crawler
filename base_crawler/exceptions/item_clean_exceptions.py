import logging
from scrapy.exceptions import DropItem

logger = logging.getLogger("item clean exceptions")


class FieldNotInItemException(DropItem):
    def __init__(self, field, item):
        super().__init__(f"Item dropped. field {field} not in item {item}")
        logger.error(f"Item dropped. field {field} not in item {item}")
