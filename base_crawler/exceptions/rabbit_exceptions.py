import logging

from scrapy.exceptions import DropItem

logger = logging.getLogger("rabbit exceptions")


class RabbitConnectionException(DropItem):
    def __init__(self):
        super().__init__("Could not create connection to rabbit mq")
        logger.critical("Could not create connection to rabbit mq")


class QueueDeclarationException(DropItem):
    def __init__(self, message):
        super().__init__(f"Queue declaration error. {message}")
        logger.critical(f"Queue declaration error. {message}")
