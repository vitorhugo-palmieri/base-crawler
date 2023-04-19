import os
import logging

import requests
from scrapy import Request

CAPTCHA_RESPONSE_NOT_READY = "CAPCHA_NOT_READY"
CAPTCHA_RESPONSE_EMPTY = ""
CAPTCHA_RESPONSE_UNSOLVABLE = "ERROR_CAPTCHA_UNSOLVABLE"
CAPTCHA_RESPONSE_TIMEOUT = "ERROR_RECAPTCHA_TIMEOUT"
CAPTCHA_RESPONSE_NO_SUCH_ID = "ERROR_NO_SUCH_CAPCHA_ID"
CAPTCHA_RESPONSE_INVALID_DOMAIN = "ERROR_RECAPTCHA_INVALID_DOMAIN"

NOT_VALID_CAPTCHA_RESPONSES = [
    CAPTCHA_RESPONSE_EMPTY,
    CAPTCHA_RESPONSE_UNSOLVABLE,
    CAPTCHA_RESPONSE_TIMEOUT,
    CAPTCHA_RESPONSE_NO_SUCH_ID,
    CAPTCHA_RESPONSE_INVALID_DOMAIN,
]

logger = logging.getLogger()


class CaptchaRequest:
    """
    For more information, check https://api.captchas.io/document/index for understanding on how to communicate with the captcha API.
    """

    def __init__(self, captcha_type):
        self.upload_url = "https://api.captchas.io/in.php"
        self.resolve_url = "https://api.captchas.io/res.php"
        self.captcha_type = captcha_type

    def _perform_captcha_v2_request(self, **kwargs):
        response = requests.post(
            url=self.upload_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "key": os.environ["CAPTCHA_API_KEY"],
                "method": "userrecaptcha",
                "googlekey": kwargs["sitekey"],
                "pageurl": kwargs["site_url"],
                "version": "v2",
                "json": "1",
                "header_acao": "0",
                "invisible": "0" if not kwargs["invisible"] else "1",
            },
        )

        return response.json()

    def _perform_captcha_image_request(self, **kwargs):
        formdata = self._build_image_formdata(**kwargs)
        response = requests.post(
            url=self.upload_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=formdata,
        )

        return response.json()

    def _build_image_formdata(self, **kwargs):
        formdata = {}
        image_type = kwargs.get("image_type", "binary")
        case_sensitive = kwargs.get("case_sensitive", True)

        if image_type == "binary":
            formdata["file"] = kwargs["image"]
        elif image_type == "base64":
            formdata["body"] = kwargs["image"]

        formdata["key"] = os.environ["CAPTCHA_API_KEY"]
        formdata["method"] = "post" if image_type == "binary" else "base64"
        formdata["json"] = "1"
        formdata["header_acao"] = "0"
        formdata["regsense"] = "0" if not case_sensitive else "1"
        return formdata

    def create_captcha_request(self, **kwargs):
        self.captcha_response = {}
        if self.captcha_type == "v2":
            while self.captcha_response.get("request") is None:
                captcha_response = self._perform_captcha_v2_request(**kwargs)
                logger.debug(f"CAPTCHA RESPONSE FROM API IS {captcha_response}")
                self.captcha_response = captcha_response
            return Request(
                url=f"{self.resolve_url}?key={os.environ['CAPTCHA_API_KEY']}&action=get&json=1&id={self.captcha_response['request']}",
                method="GET",
                meta=kwargs.get("meta"),
                dont_filter=True,
                cb_kwargs=kwargs.get("cb_kwargs"),
                callback=kwargs.get("callback"),
                errback=kwargs.get("errback"),
            )
        elif self.captcha_type == "image":
            captcha_response = self._perform_captcha_image_request(**kwargs)
            self.captcha_response = captcha_response
            return Request(
                url=f"{self.resolve_url}?key={os.environ['CAPTCHA_API_KEY']}&action=get&json=1&id={captcha_response['request']}",
                method="GET",
                meta=kwargs.get("meta"),
                dont_filter=True,
                cb_kwargs=kwargs.get("cb_kwargs"),
                callback=kwargs.get("callback"),
                errback=kwargs.get("errback"),
            )
