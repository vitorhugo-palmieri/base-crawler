import unittest

from utils import create_input_item_for_tests
from base_crawler.pipelines.transformer import procedural_class_normalizer


class ProceduralClassNormalizerTests(unittest.TestCase):
    def test_functions_return_exatly(self):
        input_item = create_input_item_for_tests(
            {
                "classeProcessual": "RECURSO INOMINADO",
            }
        )
        expected_item = create_input_item_for_tests(
            {
                "classeProcessual": "Recurso Inominado",
                "classeProcessualFilter": "Recurso Inominado",
            }
        )
        self.assertEqual(
            procedural_class_normalizer.normalize_procedural_class(input_item),
            expected_item,
        )

    def test_normalizer(self):
        inputs = [
            {"classeProcessual": "ms", "expected": "Mandado de Segurança"},
            {"classProcessual": "rOt", "expected": "Recurso Ordinário Trabalhista"},
            {"classProcessual": "ap", "expected": "Agravo de Petição"},
            {"classeProcessual": "ro", "expected": "Recurso Ordinário"},
            {"classeProcessual": "RECORD", "expected": "Recurso Ordinário"},
            {"classeProcessual": "ed", "expected": "Embargos de Declaração"},
            {
                "classeProcessual": "mandado de seguranca",
                "expected": "Mandado de Segurança",
            },
            {"classeProcessual": "RORSUM", "expected": "Recurso Ordinário Sumaríssimo"},
            {
                "classeProcessual": "airo",
                "expected": "Agravo de Instrumento em Recurso Ordinário",
            },
            {
                "classeProcessual": "AACC",
                "expected": "Ação Anulatória de Cláusulas Convencionais",
            },
            {
                "classeProcessual": "AAaaaaaffffffffffffffffffffffffffffffaaaaaaaaaasdffffffffffffff ffffffffffffffffffasssssssssssssssssssssssssssssssss ggggggggggggggggggggggggfssssssssssssssssssgggggggggg rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrCC",
                "expected": "",
            },
        ]

        for input in inputs:
            input_item = create_input_item_for_tests(input)
            result = procedural_class_normalizer.normalize_procedural_class(input_item)
            self.assertEqual(
                result["data"]["classeProcessual"], result["data"]["expected"]
            )


if __name__ == "__main__":
    unittest.main()
