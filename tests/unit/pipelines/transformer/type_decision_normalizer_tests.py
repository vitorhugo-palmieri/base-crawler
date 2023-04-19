# import unittest

# from utils import create_input_item_for_tests
# from base_crawler.pipelines.transformer import type_decision_normalizer

# class TypeDecisionNormalizer(unittest.TestCase):
#     def test_type_decision_return_correctly_in_acordao(self):
#         input_item = create_input_item_for_tests({
#             "tipoDecisao": "Acórdao"
#         })
#         expected_item = create_input_item_for_tests({
#             "tipoDecisao": "Acórdao",
#             "tipoDecisaoTreated": "Acórdão"
#         })
#         self.assertDictEqual(
#             expected_item,
#             type_decision_normalizer._normalize_type_decision(input_item)
#         )
#     def test_type_decision_return_correctly_in_monocratic_decision(self):
#         input_item = create_input_item_for_tests({
#             "tipoDecisao": "mono"
#         })
#         expected_item = create_input_item_for_tests({
#             "tipoDecisao": "mono",
#             "tipoDecisaoTreated": "Decisão Monocrática"
#         })
#         self.assertDictEqual(
#             expected_item,
#             type_decision_normalizer._normalize_type_decision(input_item)
#         )
#     def test_type_decision_return_correctly_in_sumula(self):
#         input_item = create_input_item_for_tests({
#             "tipoDecisao": "sumula"
#         })
#         expected_item = create_input_item_for_tests({
#             "tipoDecisao": "sumula",
#             "tipoDecisaoTreated": "Súmula"
#         })
#         self.assertDictEqual(
#             expected_item,
#             type_decision_normalizer._normalize_type_decision(input_item)
#         )
