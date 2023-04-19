import unittest

from utils import create_input_item_for_tests
from base_crawler.pipelines.transformer import rapporteur_normalizer


class RapporteurNormalizerTests(unittest.TestCase):
    def test_clean_before_normalize_should_return_same_rapporteur(self):
        input_item = create_input_item_for_tests({"relator": "NAME WITHOUT PREFIX"})

        self.assertDictEqual(
            input_item, rapporteur_normalizer._clean_before_normalize(input_item)
        )

    def test_clean_before_normalize_should_return_cleansed_rapporteur(self):
        rapporteur_names = [
            "DESEMBARGADOR FULAN DA SILVA",
            "DESEMBARGADORA FULAN DA SILVA",
            "DES. FULAN DA SILVA",
            "DES.(A) FULAN DA SILVA",
            "MINISTRO FULAN DA SILVA",
            "MINISTRO FULAN DA SILVA",
            "MIN. FULAN DA SILVA",
        ]
        expected_cleansed_name = "FULAN DA SILVA"

        for rn in rapporteur_names:
            input_item = create_input_item_for_tests({"relator": rn})
            result = rapporteur_normalizer._clean_before_normalize(input_item)
            self.assertEqual(expected_cleansed_name, result["data"]["relator"])

    def test_normalize_rapporteur_should_return_same_item_when_theres_no_rapporteur(
        self,
    ):
        input_item = {"data": {}}

        self.assertDictEqual(
            input_item, rapporteur_normalizer.normalize_rapporteur(input_item)
        )

    def test_normalize_rapporteur_when_is_federal(self):
        rapporteurs = [
            {
                "tribunal": "TRF1",
                "tipoDecisao": "seNtenca",
                "relator": "DESEMBARGADORA FULANO DA SILVA",
                "expected": "JUIZ(a) FED. FULANO DA SILVA",
            },
            {
                "tribunal": "TRF1",
                "relator": "MIN(A) FULANO DA SILVA",
                "expected": "DES. FED. FULANO DA SILVA",
            },
            {
                "tribunal": "TRF1",
                "relator": "FULANO DA SILVA",
                "expected": "DES. FED. FULANO DA SILVA",
            },
            {
                "tribunal": "TRF1",
                "tipoDecisao": "DECISÃO_INTERLOCUTORIA",
                "relator": "MIN(A) FULANO DA SILVA",
                "expected": "JUIZ(a) FED. FULANO DA SILVA",
            },
            {
                "tribunal": "TRESP",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "JUIZ CONVOCADO FULANO DA SILVA",
                "expected": "JUIZ(a) CONVOCADO FULANO DA SILVA",
            },
            {
                "tribunal": "TRESP",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "akkshpiranhaaeumpffpeixevorazkasgfggggdfa asdasasdfariosaofranciscoaasnnnaonaorioamazanonasnaonaopedros2",
                "expected": "",
            },
        ]

        for r in rapporteurs:
            input_item = create_input_item_for_tests(r)
            result = rapporteur_normalizer.normalize_rapporteur(input_item)
            self.assertEqual(result["data"]["relator"], result["data"]["expected"])

    def test_normalize_rapporteur_when_is_superior(self):
        rapporteurs = [
            {
                "tribunal": "STJ",
                "tipoDecisao": "setenca",
                "relator": "MINISTRO FULANO DA SILVA",
                "expected": "MIN. FULANO DA SILVA",
            },
            {
                "tribunal": "STJ",
                "tipoDecisao": "acordao",
                "relator": "FULANO DA SILVA",
                "expected": "MIN. FULANO DA SILVA",
            },
            {
                "tribunal": "STJ",
                "tipoDecisao": "decisao_interlocutoria",
                "relator": "desembargadora FULANO DA SILVA",
                "expected": "MIN. FULANO DA SILVA",
            },
            {
                "tribunal": "TSE",
                "tipoDecisao": "setenca",
                "relator": "MIN. FULANO DA SILVA",
                "expected": "MIN. FULANO DA SILVA",
            },
            {
                "tribunal": "TSE",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "MINISTRO CONVOCADO FULANO DA SILVA",
                "expected": "MIN. CONVOCADO FULANO DA SILVA",
            },
            {
                "tribunal": "TSE",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "JUIZA MINA CONVOCADA FULANO DA SILVA",
                "expected": "JUIZ(a) MINA CONVOCADA FULANO DA SILVA",
            },
            {
                "tribunal": "TSE",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "JUIZ(a) MANO CONVOCADO FULANO DA SILVA",
                "expected": "JUIZ(a) MANO CONVOCADO FULANO DA SILVA",
            },
            {
                "tribunal": "TSE",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "min DESSIRE CONVOCADO FULANO DA SILVA",
                "expected": "MIN. DESSIRE CONVOCADO FULANO DA SILVA",
            },
            {
                "tribunal": "TSE",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "JUIZ DESSIRE CONVOCADO FULANO DA SILVA",
                "expected": "JUIZ(a) DESSIRE CONVOCADO FULANO DA SILVA",
            },
            {
                "tribunal": "TSE",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "min CONVOCADO FULANO DA SILVA",
                "expected": "MIN. CONVOCADO FULANO DA SILVA",
            },
            {
                "tribunal": "TSE",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "MIN. CONVOCADO FULAaaaaaaaaaa SILVAMIN. CONVOCADO FULAaaaaaaaaaa SILVAMIN. CONVOCADO FULAaaaaaaaaaa SILVAmissssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssn CONVOCADO FULANO DA SILVA",
                "expected": "",
            },
            {
                "tribunal": "STF",
                "relator": "ABNER DE VASCONCELOS - CONVOCADO",
                "expected": "JUIZ(a) ABNER DE VASCONCELOS  CONVOCADO",
            },
        ]

        for r in rapporteurs:
            input_item = create_input_item_for_tests(r)
            result = rapporteur_normalizer.normalize_rapporteur(input_item)
            self.assertEqual(result["data"]["relator"], result["data"]["expected"])

    def test_normalize_rapporteur_when_is_state(self):
        rapporteurs = [
            {
                "tribunal": "TRT2",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "JUIZ FULANINHO DA SILVA",
                "expected": "JUIZ(a) FULANINHO DA SILVA",
            },
            {
                "tribunal": "TRT15",
                "tipoDecisao": "sentencas",
                "relator": "MINISTRO FULAN DA SILVA",
                "expected": "JUIZ(a) FULAN DA SILVA",
            },
            {
                "tribunal": "TRERJ",
                "relator": "juiz FULANINHO DA SILVA",
                "expected": "DES. FULANINHO DA SILVA",
            },
            {
                "tribunal": "TRESP",
                "relator": "Desembargador FULANAO DA SILVA",
                "expected": "DES. FULANAO DA SILVA",
            },
            {
                "tribunal": "TRT9",
                "relator": "juiza MANO CONVOCADO FULANO DA SILVA",
                "expected": "JUIZ(a) MANO CONVOCADO FULANO DA SILVA",
            },
            {
                "tribunal": "TRT5",
                "tipoDecisao": "decisao interlocutoria",
                "relator": "DES MANO CONVOCADO FULANO DA SILVA 1",
                "expected": "DES. MANO CONVOCADO FULANO DA SILVA 1",
            },
            {
                "tribunal": "TRT5",
                "relator": "desª Mina  FULANO DA SILVA",
                "expected": "DES. Mina  FULANO DA SILVA",
            },
            {
                "tribunal": "TRF1",
                "relator": "JUIZ DERIVALDO DE FIGUEIREDO BEZERRA FILHO (CONV.)",
                "expected": "JUIZ(a) DERIVALDO DE FIGUEIREDO BEZERRA FILHO (CONV.)",
            },
            {
                "tribunal": "TRF3",
                "relator": "JUÍZA CONVOCADA CARLA RISTER",
                "expected": "JUIZ(a) CONVOCADA CARLA RISTER",
            },
            {
                "tribunal": "TRF3",
                "relator": "JUIZ CONVOCADO CARLOS MOTTA",
                "expected": "JUIZ(a) CONVOCADO CARLOS MOTTA",
            },
            {
                "tribunal": "TRF1",
                "relator": "JUIZ FEDERAL CÉSAR CINTRA JATAHY FONSECA (CONV.)",
                "expected": "JUIZ(a) FED. CÉSAR CINTRA JATAHY FONSECA (CONV.)",
            },
        ]

        for r in rapporteurs:
            input_item = create_input_item_for_tests(r)

            result = rapporteur_normalizer.normalize_rapporteur(input_item)
            self.assertEqual(result["data"]["relator"], result["data"]["expected"])


if __name__ == "__main__":
    unittest.main()
