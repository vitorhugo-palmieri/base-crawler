import unittest

from twisted.internet import defer
from freezegun import freeze_time

from tests.spiders.mock_spider_success import (
    MockSpiderSuccess,
    MockSpiderCaptchaV2,
    MockSpiderCaptchaImage,
    MockSpiderMultipleItems,
)
from tests.spiders.mock_spider_file_upload import (
    MockSpiderUploadText,
    MockSpiderUploadPdf,
    MockSpiderUploadHtml,
)
from tests.spiders.mock_spider_pipeline_error import MockSpiderPipelineError
from tests.spiders.mock_spider_navigation_error import (
    MockSpiderNotFound,
    MockSpiderInvalidPage,
    MockSpiderInvalidInput,
)
from tests.integration_test_fixture import IntegrationTestFixture


class SpiderIntegrationTests(IntegrationTestFixture):
    def setUp(self):
        self.setup_crawler(
            settings={
                "ITEM_PIPELINES": {
                    "base_crawler.pipelines.item_prepare_pipeline.ItemPreparePipeline": 100,
                    "base_crawler.pipelines.schema_validation_pipeline.SchemaValidationPipeline": 200,
                    "base_crawler.pipelines.mongo_pipeline.MongoPipeline": 300,
                    "base_crawler.pipelines.transformer.transformer_pipeline.TransformerPipeline": 400,
                    "base_crawler.pipelines.elastic_pipeline.ElasticPipeline": 500,
                }
            }
        )

    def tearDown(self):
        self.tear_down_outputs_database("mock-spider-success")
        self.tear_down_transformed_outputs_database("mock-spider-success")
        self.tear_down_errors_database("mock-spider-success")
        self.tear_down_outputs_database("mock-spider-captcha-v2")
        self.tear_down_transformed_outputs_database("mock-spider-captcha-v2")
        self.tear_down_errors_database("mock-spider-captcha-v2")
        self.tear_down_outputs_database("mock-spider-captcha-image")
        self.tear_down_transformed_outputs_database("mock-spider-captcha-image")
        self.tear_down_errors_database("mock-spider-captcha-image")
        self.tear_down_outputs_database("mock-spider-upload-text")
        self.tear_down_transformed_outputs_database("mock-spider-upload-text")
        self.tear_down_errors_database("mock-spider-upload-text")
        self.tear_down_outputs_database("mock-spider-upload-pdf")
        self.tear_down_transformed_outputs_database("mock-spider-upload-pdf")
        self.tear_down_errors_database("mock-spider-upload-pdf")
        self.tear_down_outputs_database("mock-spider-upload-html")
        self.tear_down_transformed_outputs_database("mock-spider-upload-html")
        self.tear_down_errors_database("mock-spider-upload-html")
        self.tear_down_outputs_database("mock-spider-multiple")
        self.tear_down_transformed_outputs_database("mock-spider-multiple")
        self.tear_down_errors_database("mock-spider-multiple")
        self.tear_down_outputs_database("mock-spider-fail")
        self.tear_down_transformed_outputs_database("mock-spider-fail")
        self.tear_down_errors_database("mock-spider-fail")
        self.tear_down_outputs_database("mock-spider-not-found")
        self.tear_down_transformed_outputs_database("mock-spider-not-found")
        self.tear_down_errors_database("mock-spider-not-found")
        self.tear_down_outputs_database("mock-spider-invalid-page")
        self.tear_down_transformed_outputs_database("mock-spider-invalid-page")
        self.tear_down_errors_database("mock-spider-invalid-page")
        self.tear_down_outputs_database("mock-spider-invalid-input")
        self.tear_down_transformed_outputs_database("mock-spider-invalid-input")
        self.tear_down_errors_database("mock-spider-invalid-input")

    def _get_expected_multiple_items(self):
        expected_items_multiple = []
        ids = [
            "cfcd208495d565ef66e7dff9f98764da",
            "c4ca4238a0b923820dcc509a6f75849b",
            "c81e728d9d4c2f636f067f89cc14862c",
            "eccbc87e4b5ce2fe28308fd9f2a7baf3",
            "a87ff679a2f3e71d9181a67b7542122c",
        ]
        for i in range(0, 5):
            expected_items_multiple.append(
                {
                    "_id": ids[i],
                    "data": {
                        "idField": i,
                        "testKey": "TESTVALUE",
                    },
                    "metadata": {
                        "processingDate": "2021-01-01T03:00:00+00:00",
                        "spiderName": "mock-spider-multiple",
                        "input": {"a": "b"},
                    },
                }
            )
        return expected_items_multiple

    def _get_multiple_lookups(self):
        lookups = []
        for i in range(0, 5):
            lookups.append({"data.idField": i})
        return lookups

    @defer.inlineCallbacks
    def _run_crawler(self, crawler):
        yield self.process.crawl(crawler["crawler"], input=crawler["input"])
        defer.returnValue(self._assert_crawler(crawler))

    def _create_crawler(self, crawler_class, **kwargs):
        """
        This method creates a crawler and the objects to be asserted when the deferred crawler returns a value, either by yielding items or raising exceptions.
        """
        finish_reason = kwargs.get("finish_reason")
        pipeline_error = kwargs.get("pipeline_error")
        assert_item_found = kwargs.get("assert_item_found")
        assert_multiple_items = kwargs.get("assert_multiple_items")
        crawler_input = kwargs.get("crawler_input")
        expected_item = kwargs.get("expected_item")
        lookup = kwargs.get("lookup")
        return {
            "crawler": self.process.create_crawler(crawler_class),
            "input": crawler_input,
            "finish_reason": finish_reason,
            "pipeline_error": pipeline_error,
            "assert_item_found": assert_item_found,
            "assert_multiple_items": assert_multiple_items,
            "expected_item": expected_item,
            "lookup": lookup,
        }

    def _create_crawlers(self):
        """
        This method is used to create crawler objects to be started and asserted. It must return na array of objects returned by the _create_crawler method.
        """
        expected_items_multiple = self._get_expected_multiple_items()
        lookups_multiple = self._get_multiple_lookups()
        return [
            self._create_crawler(
                MockSpiderSuccess,
                finish_reason="finished",
                pipeline_error=False,
                assert_item_found=True,
                expected_item={
                    "_id": "e9de89b0a5e9ad6efd5e5ab543ec617c",
                    "data": {"testKey": "TESTVALUE"},
                    "metadata": {
                        "processingDate": "2021-01-01T03:00:00+00:00",
                        "spiderName": "mock-spider-success",
                        "input": {"a": "b"},
                    },
                },
                lookup={"data.testKey": "TESTVALUE"},
            ),
            self._create_crawler(
                MockSpiderMultipleItems,
                finish_reason="finished",
                pipeline_error=False,
                assert_multiple_items=True,
                expected_item=expected_items_multiple,
                lookup=lookups_multiple,
            ),
            self._create_crawler(
                MockSpiderPipelineError,
                finish_reason="finished",
                pipeline_error=True,
                assert_item_found=False,
                expected_item={
                    "_id": "e9de89b0a5e9ad6efd5e5ab543ec617c",
                    "data": {"testKey": "TESTVALUE"},
                    "metadata": {
                        "processingDate": "2021-01-01T03:00:00+00:00",
                        "spiderName": "mock-spider-pipeline-error",
                        "input": {"a": "b"},
                    },
                },
                lookup={"data.testKey": "TESTVALUE"},
            ),
            self._create_crawler(
                MockSpiderNotFound,
                finish_reason="Input was not found in source",
                pipeline_error=False,
                assert_item_found=False,
                expected_item={
                    "_id": "e9de89b0a5e9ad6efd5e5ab543ec617c",
                    "data": {"testKey": "TESTVALUE"},
                    "metadata": {
                        "processingDate": "2021-01-01T03:00:00+00:00",
                        "spiderName": "mock-spider-not-found",
                        "input": {"a": "b"},
                    },
                },
                lookup={"data.testKey": "TESTVALUE"},
            ),
            self._create_crawler(
                MockSpiderInvalidPage,
                finish_reason="Page is invalid - {}",
                pipeline_error=False,
                assert_item_found=False,
            ),
            self._create_crawler(
                MockSpiderInvalidInput,
                finish_reason="Input received 'input' is invalid",
                pipeline_error=False,
                assert_item_found=False,
                crawler_input="input",
            ),
            self._create_crawler(
                MockSpiderCaptchaV2,
                finish_reason="finished",
                pipeline_error=False,
                assert_item_found=True,
                expected_item={
                    "_id": "e8a8cbabc52387bfb26f739528def782",
                    "data": {"testKey": "TESTVALUECAPTCHAV2"},
                    "metadata": {
                        "processingDate": "2021-01-01T03:00:00+00:00",
                        "spiderName": "mock-spider-captcha-v2",
                        "input": {"a": "b"},
                    },
                },
                lookup={"data.testKey": "TESTVALUECAPTCHAV2"},
            ),
            self._create_crawler(
                MockSpiderUploadText,
                finish_reason="finished",
                pipeline_error=False,
                assert_item_found=True,
                expected_item={
                    "_id": "e9de89b0a5e9ad6efd5e5ab543ec617c",
                    "data": {"testKey": "TESTVALUE"},
                    "metadata": {
                        "processingDate": "2021-01-01T03:00:00+00:00",
                        "spiderName": "mock-spider-upload-text",
                        "input": {"a": "b"},
                    },
                },
                lookup={"data.testKey": "TESTVALUE"},
            ),
            self._create_crawler(
                MockSpiderUploadPdf,
                finish_reason="finished",
                pipeline_error=False,
                assert_item_found=True,
                expected_item={
                    "_id": "e9de89b0a5e9ad6efd5e5ab543ec617c",
                    "data": {"testKey": "TESTVALUE"},
                    "metadata": {
                        "processingDate": "2021-01-01T03:00:00+00:00",
                        "spiderName": "mock-spider-upload-pdf",
                        "input": {"a": "b"},
                    },
                },
                lookup={"data.testKey": "TESTVALUE"},
            ),
            self._create_crawler(
                MockSpiderUploadHtml,
                finish_reason="finished",
                pipeline_error=False,
                assert_item_found=True,
                expected_item={
                    "_id": "e9de89b0a5e9ad6efd5e5ab543ec617c",
                    "data": {"testKey": "TESTVALUE"},
                    "metadata": {
                        "processingDate": "2021-01-01T03:00:00+00:00",
                        "spiderName": "mock-spider-upload-html",
                        "input": {"a": "b"},
                    },
                },
                lookup={"data.testKey": "TESTVALUE"},
            ),
        ]

    def _assert_crawler(self, crawler):
        """
        This method performs assertions on the crawler object created by the _create_crawler function. This method is called only after a deferred crawler returns a value.
        """
        if crawler["assert_item_found"]:
            self._assert_item_found(
                crawler["crawler"].spider.name,
                crawler["expected_item"],
                crawler["lookup"],
            )
        elif crawler["assert_multiple_items"]:
            self._assert_multiple_items_found(
                crawler["crawler"].spider.name,
                crawler["expected_item"],
                crawler["lookup"],
            )
        else:
            self._assert_item_not_found(
                crawler["crawler"].spider.name, crawler["lookup"]
            )
        if crawler["pipeline_error"]:
            self._assert_pipeline_error(
                crawler["crawler"].spider.name,
                crawler["crawler"].stats,
                crawler["lookup"],
            )

        self._assert_spider_finish_reason(
            crawler["crawler"].stats, crawler["finish_reason"]
        )

    @freeze_time(
        "2021-01-01 00:00:00", ignore=["logging", "scrapy", "requests", "twisted"]
    )
    def test_spiders(self):
        crawlers = self._create_crawlers()
        for crawler in crawlers:
            self._run_crawler(crawler)
        self.process.start()


if __name__ == "__main__":
    unittest.main()
