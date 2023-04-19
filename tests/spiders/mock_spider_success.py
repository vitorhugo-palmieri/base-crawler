import base64
import scrapy

from base_crawler.helper import body_to_soup
from base_crawler.helper import load_json
from base_crawler.requests import captcha_requests
from base_crawler.spiders.base_spider import BaseSpider


class MockSpiderSuccess(BaseSpider):
    name = "mock-spider-success"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["testKey"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = {"a": "b"}

    def start_requests(self):
        yield scrapy.Request(url="http://example.com", callback=self.parse)

    def parse(self, response):
        yield {"testKey": "testvalue"}


class MockSpiderMultipleItems(BaseSpider):
    name = "mock-spider-multiple"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["idField"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = {"a": "b"}

    def start_requests(self):
        yield scrapy.Request(url="http://example.com", callback=self.parse)

    def parse(self, response):
        for i in range(0, 5):
            yield {"testKey": "testvalue", "idField": i}


class MockSpiderCaptchaV2(BaseSpider):
    name = "mock-spider-captcha-v2"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["testKey"]
    custom_settings = {"DOWNLOAD_DELAY": 2}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = {"a": "b"}

    def start_requests(self):
        self.logger.info("START REQUESTS CAPTCHA V2")
        yield scrapy.Request(
            url="https://esaj.tjsp.jus.br/cpopg/open.do",
            dont_filter=True,
            callback=self._on_first_page,
        )

    def _on_first_page(self, response):
        self.logger.info("FIRST PAGE CAPTCHA V2")
        site_key = (
            body_to_soup(response.body)
            .find("div", class_="g-recaptcha")
            .get("data-sitekey")
        )

        self.captcha_poll_request = captcha_requests.CaptchaRequest(
            captcha_type="v2"
        ).create_captcha_request(
            sitekey=site_key,
            site_url="https://esaj.tjsp.jus.br/cpopg/open.do",
            dont_filter=True,
            invisible=False,
            callback=self._on_captcha_response,
        )

        yield self.captcha_poll_request

    def _on_captcha_response(self, response):
        captcha_response = load_json(response.body)
        self.logger.info(f"CAPTCHA V2 RESPONSE IS {captcha_response}")
        if captcha_response["status"] != captcha_requests.CAPTCHA_RESPONSE_READY:
            return self.captcha_poll_request
        assert captcha_response["status"] == captcha_requests.CAPTCHA_RESPONSE_READY
        assert "status" in captcha_response
        return {"testKey": "testvaluecaptchav2"}


class MockSpiderCaptchaImage(BaseSpider):
    name = "mock-spider-captcha-image"
    required_keys = ["testKey"]
    schema_name = "mock_spider_schema"
    schema_path = "/app/tests/schemas/"
    id_fields = ["testKey"]
    custom_settings = {"DOWNLOAD_DELAY": 2}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = {"a": "b"}

    def start_requests(self):
        self.logger.info("START REQUESTS CAPTCHA IMAGE")
        yield scrapy.Request(
            url="https://www5.tjmg.jus.br/jurisprudencia/formEspelhoAcordao.do",
            callback=self._on_first_page,
        )

    def _on_first_page(self, response):
        self.logger.info("FIRST PAGE CAPTCHA IMAGE")
        yield scrapy.Request(
            url="https://www5.tjmg.jus.br/jurisprudencia/pesquisaPalavrasEspelhoAcordao.do?numeroRegistro=1&totalLinhas=1&palavras=&pesquisarPor=ementa&orderByData=2&codigoOrgaoJulgador=&listaOrgaoJulgador=1-1&codigoCompostoRelator=&classe=&codigoAssunto=&dataPublicacaoInicial=20%2F01%2F2019&dataPublicacaoFinal=20%2F01%2F2019&dataJulgamentoInicial=&dataJulgamentoFinal=&siglaLegislativa=&referenciaLegislativa=Clique+na+lupa+para+pesquisar+as+refer%EAncias+cadastradas...&numeroRefLegislativa=&anoRefLegislativa=&legislacao=&norma=&descNorma=&complemento_1=&listaPesquisa=&descricaoTextosLegais=&observacoes=&linhasPorPagina=10&pesquisaPalavras=Pesquisar",
            dont_filter=True,
            meta={"handle_httpstatus_list": [401]},
            callback=self._on_search_captcha,
        )

    def _on_search_captcha(self, response):
        self.logger.info("SEARCH PAGE CAPTCHA IMAGE")

        captcha_image_url = (
            body_to_soup(response.body).find("img", id="captcha_image").get("src")
        )

        yield scrapy.Request(
            url=f"https://www5.tjmg.jus.br/jurisprudencia/{captcha_image_url}",
            dont_filter=True,
            callback=self._on_image_page,
        )

    def _on_image_page(self, response):
        self.logger.info("ON IMAGE PAGE")

        base64_image = base64.b64encode(response.body)
        self.captcha_poll_request = captcha_requests.CaptchaRequest(
            captcha_type="image"
        ).create_captcha_request(
            image=base64_image, image_type="base64", callback=self._on_captcha_response
        )
        yield self.captcha_poll_request

    def _on_captcha_response(self, response):
        self.logger.info("ON CAPTCHA IMAGE RESPONSE")
        captcha_response = load_json(response.body)
        self.logger.info(f"CAPTCHA IMAGE RESPONSE IS {captcha_response}")
        if captcha_response["request"] == captcha_requests.CAPTCHA_RESPONSE_NOT_READY:
            return self.captcha_poll_request
        assert (
            captcha_response["request"] != captcha_requests.CAPTCHA_RESPONSE_NOT_READY
        )
        assert "request" in captcha_response
        return {"testKey": "testvaluecaptchaimage"}
