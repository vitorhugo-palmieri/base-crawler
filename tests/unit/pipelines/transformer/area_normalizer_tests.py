import unittest

from utils import create_input_item_for_tests
from base_crawler.pipelines.transformer import area_normalizer


class AreaNormalizerTests(unittest.TestCase):
    def test_get_area_from_jurisprudence_class_should_return_the_same_input(self):
        input_item = create_input_item_for_tests({"tribunal": "TJRJ"})

        self.assertDictEqual(
            input_item, area_normalizer._get_area_from_jurisprudence_class(input_item)
        )

    def test_normalize_area_when_area_doesnt_exists(self):
        input_item = create_input_item_for_tests({})

        self.assertDictEqual(input_item, area_normalizer.normalize_area(input_item))

    def test_normalize_area_when_area_exists(self):
        pass


if __name__ == "__main__":
    unittest.main()
