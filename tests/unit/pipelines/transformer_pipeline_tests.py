import unittest
from base_crawler import helper
from base_crawler.pipelines.transformer.transformer_pipeline import TransformerPipeline
from tests.spiders.mock_spider_success import MockSpiderSuccess

class TransformerPipelineTests(unittest.TestCase):
    def setUp(self):
        self.pipeline = TransformerPipeline()
        self.spider = MockSpiderSuccess()
        self.maxDiff = None

    def test_transform_pipeline_should_process_item_correctly(self):
        input_item = {
            "_id":"ccfdd0e0acb279a0b17124292968843f",
            "data": {
                "tribunal": "TRF1",
                "relator": "DESEMBARGADOR DANIEL ORIVALDO DA SILVA",
                "ementa": "<p style='blue'>     APELAÇÃO CÍVEL.</p> DIREITO        PÚBLICO. Provido",
                "tipoDecisao":"Acordao"
            }
        }

        expected_item = {
            "_id":"ccfdd0e0acb279a0b17124292968843f",
            "data": {
                "tribunal": "TRF1",
                "relator": "DANIEL ORIVALDO DA SILVA",
                "ementa": "<p style='blue'>      direito civel APELAÇÃO CÍVEL.</p> DIREITO        PÚBLICO. Provido",
                "areaTreated": "ADMINISTRATIVO / PÚBLICO",
                "relatorTreated": "DES. FED. DANIEL ORIVALDO DA SILVA",
                "ementaTreated": "APELAÇÃO CÍVEL. DIREITO PÚBLICO.",
                "tipoDecisao":"Acordao",
                "tipoDecisaoTreated":"Acórdão",
                "provimento":"PROVIDO"
            }
        }

        actual_item = self.pipeline.process_item(input_item, self.spider)
        found_item = helper.find_item_in_database("transformed_outputs", self.spider.name, actual_item)
        self.assertDictEqual(expected_item, found_item)
        self.assertDictEqual(expected_item, input_item)
