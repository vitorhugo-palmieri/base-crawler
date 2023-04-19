import os
import logging
import requests

from time import sleep
from scrapy import Request
from scrapy.http import JsonRequest
from base_crawler.exceptions.spider_exceptions import CaptchaResponseError
from capmonster_python import RecaptchaV2Task

CAPTCHA_RESPONSE_READY = "ready"
CAPTCHA_RESPONSE_NOT_READY = "CAPCHA_NOT_READY"
CAPTCHA_RESPONSE_INVALID_SITEKEY = "ERROR_RECAPTCHA_INVALID_SITEKEY"
CAPTCHA_RESPONSE_EMPTY = ""
CAPTCHA_RESPONSE_UNSOLVABLE = "ERROR_CAPTCHA_UNSOLVABLE"
CAPTCHA_RESPONSE_TIMEOUT = "ERROR_RECAPTCHA_TIMEOUT"
CAPTCHA_RESPONSE_NO_SUCH_ID = "ERROR_NO_SUCH_CAPCHA_ID"
CAPTCHA_RESPONSE_INVALID_DOMAIN = "ERROR_RECAPTCHA_INVALID_DOMAIN"

logger = logging.getLogger()


class CaptchaRequest:
    """
    For more information, check https://zennolab.atlassian.net/wiki/spaces/APIS/pages/491575/English+Documentation for understanding on how to communicate with the captcha API.
    """

    def __init__(self, captcha_type):
        self.captcha_type = captcha_type

    def _generate_get_captcha_result_request(self, task_id, captcha_key, **kwargs):
        return JsonRequest(
            url=f"{self.captcha_provider_base_url}/getTaskResult",
            method="POST",
            data={"clientKey": captcha_key, "taskId": task_id},
            meta=kwargs.get("meta"),
            dont_filter=True,
            cb_kwargs=kwargs.get("cb_kwargs"),
            callback=kwargs.get("callback"),
            errback=kwargs.get("errback"),
        )

    def _perform_captcha_create_task_v3_request(self, **kwargs):
        response = requests.post(
            url=f"{self.captcha_provider_base_url}/createTask",
            headers={"Content-Type": "application/json"},
            json={
                "clientKey": os.environ["ANTI_CAPTCHA_API_KEY"],
                "task": {
                    "type": "RecaptchaV3TaskProxyless",
                    "websiteKey": kwargs["sitekey"],
                    "websiteURL": kwargs["site_url"],
                    "minScore": kwargs["minScore"],
                    "pageAction": kwargs["action"],
                    "isEnterprise": False,
                },
            },
        )

        return response.json()

    def _perform_captcha_v3_request(self, **kwargs):
        response = requests.post(
            url=f"{self.captcha_provider_base_url}/createTask",
            headers={"Content-Type": "application/json"},
            json={
                "clientKey": os.environ["ANTI_CAPTCHA_API_KEY"],
                "task": {
                    "type": "RecaptchaV3TaskProxyless",
                    "websiteKey": kwargs["sitekey"],
                    "websiteURL": kwargs["site_url"],
                    "minScore": kwargs["minScore"],
                    "pageAction": kwargs["action"],
                    "isEnterprise": False,
                },
            },
        )

        return response.json()

    def _captcha_v3(self, **kwargs):
        self.captcha_provider_base_url = "https://api.anti-captcha.com"

        captcha_task_create_response = self._perform_captcha_v3_request(**kwargs)
        logger.debug(
            f"CAPTCHA CREATE TASK v3 RESPONSE FROM API IS {captcha_task_create_response}"
        )

        task_id = captcha_task_create_response.get("taskId")
        if task_id is None:
            raise CaptchaResponseError()
        sleep(3)

        return self._generate_get_captcha_result_request(
            task_id, os.environ["ANTI_CAPTCHA_API_KEY"], **kwargs
        )

    def _perform_captcha_v2_request(self, **kwargs):
        response = requests.post(
            url=f"{self.captcha_provider_base_url}/createTask",
            headers={"Content-Type": "application/json"},
            json={
                "clientKey": os.environ["CAPTCHA_API_KEY"],
                "task": {
                    "type": "NoCaptchaTaskProxyless",
                    "websiteKey": kwargs["sitekey"],
                    "websiteURL": kwargs["site_url"],
                },
            },
        )

        return response.json()

    def _captcha_v2(self, **kwargs):
        self.captcha_provider_base_url = "https://api.capmonster.cloud"
        while captcha_response.get("taskId") is None:
            captcha_response = self._perform_captcha_v2_request(**kwargs)
            logger.debug(f"CAPTCHA v2 RESPONSE FROM API IS {captcha_response}")
            captcha_response = captcha_response
        return self._generate_get_captcha_result_request(
            captcha_response["taskId"], os.environ["CAPTCHA_API_KEY"], **kwargs
        )

    def _perform_captcha_img_request(self, **kwargs):
        response = requests.post(
            url=f"{self.captcha_provider_base_url}/createTask",
            headers={"Content-Type": "application/json"},
            json={
                "clientKey": os.environ["CAPTCHA_API_KEY"],
                "task": {"type": "ImageToTextTask", "body": kwargs["base64"]},
            },
        )

        return response.json()

    def _captcha_img(self, **kwargs):
        self.captcha_provider_base_url = "https://api.capmonster.cloud"
        captcha_response = {}

        while captcha_response.get("taskId") is None:
            captcha_response = self._perform_captcha_img_request(**kwargs)
            logger.debug(f"CAPTCHA IMAGE RESPONSE FROM API IS {captcha_response}")
            captcha_response = captcha_response
        return self._generate_get_captcha_result_request(
            captcha_response["taskId"], os.environ["CAPTCHA_API_KEY"], **kwargs
        )

    def create_captcha_request(self, **kwargs):
        if self.captcha_type == "image":
            return self._captcha_img(**kwargs)
        if self.captcha_type == "v2":
            return self._captcha_v2(**kwargs)
        elif self.captcha_type == "v3":
            return self._captcha_v3(**kwargs)
