import unittest
import utils
from base_crawler.pipelines.transformer import summary_normalizer


class SummaryNormalizerTests(unittest.TestCase):
    def test_replace_extra_space_should_return_cleaned_text(self):
        summary = "APELAÇÃO CÍVEL.             DIREITO PÚBLICO.         AÇÃO INDENIZATÓRIA.            ALEGAÇÃO DE         INDEVIDA DESTRUIÇÃO DE ARMA DE FOGO"
        EXPECTED_SUMMARY = "APELAÇÃO CÍVEL. DIREITO PÚBLICO. AÇÃO INDENIZATÓRIA. ALEGAÇÃO DE INDEVIDA DESTRUIÇÃO DE ARMA DE FOGO"

        self.assertEqual(
            EXPECTED_SUMMARY, summary_normalizer._replace_extra_space(summary)
        )

    def test_remove_tags_html_should_return_text_without_html(self):
        summary = "<p style='blue'>APELAÇÃO CÍVEL.</p> DIREITO PÚBLICO. AÇÃO INDENIZATÓRIA. ALEGAÇÃO DE INDEVIDA DESTRUIÇÃO DE <b class=\"negritoDestacado\">ARMA</b> DE FOGO"
        EXPECTED_SUMMARY = "APELAÇÃO CÍVEL. DIREITO PÚBLICO. AÇÃO INDENIZATÓRIA. ALEGAÇÃO DE INDEVIDA DESTRUIÇÃO DE ARMA DE FOGO"

        self.assertEqual(
            EXPECTED_SUMMARY, summary_normalizer._remove_tags_html(summary)
        )

    def test_normalize_summary_should_return_same_item_when_theres_no_summary(self):
        input_item = {"data": {}}

        self.assertDictEqual(
            input_item, summary_normalizer.normalize_summary(input_item)
        )

    def test_remove_brake_lines(self):
        EXPECTED_SUMMARY = "TRIBUTÁRIO. APELAÇÃO CÍVEL. EMBARGOS À EXECUÇÃO. IPTU. IMUNIDADE DE TEMPLOS DE QUALQUER CULTO. APLICAÇÃO DO ART. 150, VI, “b” DA CONSTITUIÇÃO FEDERAL."
        inputs = [
            {
                "tribunal": "TJSP",
                "ementa": "CONTRIBUIÇÃO PARA O PIS/PASEPPeríodo de apuração: 01/10/2009 a 31/12/2009FRAUDE. DISSIMULAÇÃO. DESCONSIDERAÇÃO DE NEGÓCIO ILÍCITO.Comprovada a existência de simulação/dissimulação, por meio de interposta pessoa, com o fim exclusivo de afastar o pagamento da contribuição devida, é correta a glosa dos créditos oriundos de tal fraude, tendo como consequência a desconsideração do negócio fraudulento e a recomposição da escrita contábil e fiscal para aferição da contribuição devida.CRÉDITOS BÁSICOS. OPERAÇÕES SIMULADAS. GLOSAS.Comprovado, que as operações de compras dos bens que geraram os créditos aproveitados foram simuladas glosam- se os valores indevidamente creditados.USO DE INTERPO",
                "expected":"TRIBUTÁRIO. APELAÇÃO CÍVEL.EMBARGOS À EXECUÇÃO",
            },
            # {
            #     "tribunal": "TJPR",
            #     "ementa": "TRIBUTÁRIO.\nAPELAÇÃO CÍVEL. EMBARGOS À\n\n\nEXECUÇÃO. IPTU.\n<b>IMUNIDADE</b> DE TEMPLOS DE QUALQUER CULTO. APLICAÇÃO DO\nART. 150, VI, “b” DA CONSTITUIÇÃO FEDERAL.",
            #     "expected": "TRIBUTÁRIO. APELAÇÃO CÍVEL. EMBARGOS À EXECUÇÃO. IPTU. IMUNIDADE DE TEMPLOS DE QUALQUER CULTO. APLICAÇÃO DO ART. 150, VI, “b” DA CONSTITUIÇÃO FEDERAL.",
            # },
            # {
            #     "tribunal": "TJPR",
            #     "ementa": "3\n\n\n\n\n\n\n\n\n VIOLÊNCIA\n  DOMÉSTICA.\n\n\n\n AMEAÇA.\n\n MEDIDAS\nPROTETIVAS DE URGÊNCIA.",
            #     "expected": "3 VIOLÊNCIA DOMÉSTICA. AMEAÇA. MEDIDAS PROTETIVAS DE URGÊNCIA.",
            # },
        ]
        for input in inputs:
            input = utils.create_input_item_for_tests(input)

            self.assertEqual(
                input["data"]["expected"],
                summary_normalizer.normalize_summary(input)["data"]["ementa"],
            )


if __name__ == "__main__":
    unittest.main()
