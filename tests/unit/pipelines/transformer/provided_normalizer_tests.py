import unittest

from utils import create_input_item_for_tests
from base_crawler.pipelines.transformer import provided_normalizer
from utils import EMENTAS


class ProvidedNormalizerTests(unittest.TestCase):
    def test_provided_return_correctly_provided(self):
        input_item = create_input_item_for_tests({"ementa": EMENTAS[0]})
        expected_item = create_input_item_for_tests(
            {"ementa": EMENTAS[0], "provimento": "PROVIDO"}
        )
        self.assertDictEqual(
            expected_item, provided_normalizer._find_provided(input_item)
        )

    def test_provided_return_correctly_not_provided(self):
        input_item = create_input_item_for_tests({"ementa": EMENTAS[2]})
        expected_item = create_input_item_for_tests(
            {"ementa": EMENTAS[2], "provimento": "NÃO PROVIDO"}
        )
        self.assertDictEqual(
            expected_item, provided_normalizer._find_provided(input_item)
        )

    def test_input(self):
        inputs = [
            {
                "ementa": EMENTAS[3],
                "expeted": "PARCIALMENTE PROVIDO",
            },
            {
                "ementa": EMENTAS[4],
                "expeted": "PARCIALMENTE PROVIDO",
            },
        ]
        for input in inputs:
            input = create_input_item_for_tests(input)
            self.assertEqual(
                provided_normalizer.normalize_provided(input)
                .get("data")
                .get("provimento"),
                input.get("data").get("expeted"),
            )


if __name__ == "__main__":
    unittest.main()
