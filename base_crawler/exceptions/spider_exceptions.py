import logging
from scrapy.exceptions import DropItem
from scrapy.exceptions import CloseSpider

logger = logging.getLogger(__name__)


class CreateSpiderException(Exception):
    def __init__(self):
        super().__init__("Could not create spider. Check required_keys field.")
        logger.critical("Could not create spider. Check required_keys field.")


class OutputException(DropItem):
    def __init__(self, message):
        super().__init__(f"Required key {message} not in item")
        logger.critical(f"Required key {message} not in item")


class InvalidSpiderAttributesException(DropItem):
    def __init__(self, message):
        super().__init__(f"Check your spider attributes. {message}")
        logger.critical(f"Check your spider attributes. {message}")


class InvalidInput(CloseSpider):
    def __init__(self, input_received):
        super().__init__(f"Input received '{input_received}' is invalid")
        logger.error(f"Input received '{input_received}' is invalid")


class InputNotFound(CloseSpider):
    def __init__(self):
        super().__init__("Input was not found in source")
        logger.error("Input was not found in source")


class InvalidPage(CloseSpider):
    def __init__(self, message="Page is invalid", response_url=""):
        super().__init__(f"{message} - {response_url}")
        logger.error(f"{message} - {response_url}")


class InputAlreadyCollected(CloseSpider):
    def __init__(self):
        super().__init__("All items in this input have been collected")
        logger.error("All items in this input have been collected")


class CaptchaResponseError(CloseSpider):
    def __init__(self):
        super().__init__("Captcha Response Error")
        logger.error("Captcha Response Error")
