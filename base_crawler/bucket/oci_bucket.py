import os

import scrapy

_HEADERS_BY_EXTENSION = {
    "pdf": "application/pdf",
    "html": "text/html",
    "rtf": "application/rtf",
    "doc": "application/msword",
    "docx": "application/msword",
    "txt": "text/plain",
}


def _get_header_by_extension(extension):
    return _HEADERS_BY_EXTENSION.get(extension, "application/octet-stream")


class OracleBucketManager:
    def __init__(self):
        self.bucket_url = os.environ.get("BUCKET_URL")

    def create_put_bucket_request(self, **kwargs):
        file_content = kwargs["file_content"]
        file_name = kwargs["file_name"]

        extension = file_name.split(".")[-1]

        headers = {"Content-Type": _get_header_by_extension(extension)}

        return scrapy.Request(
            url=self.bucket_url + file_name,
            method="PUT",
            headers=headers,
            body=file_content,
            meta=kwargs.get("meta"),
            dont_filter=True,
            cb_kwargs=kwargs.get("cb_kwargs"),
            callback=kwargs["callback"],
            errback=kwargs["errback"],
        )
