from base_crawler.exceptions.transformer_exceptions import TransformerPipelineException
from .rapporteur_normalizer import normalize_rapporteur
from .area_normalizer import normalize_area
from .summary_normalizer import normalize_summary
from .provided_normalizer import normalize_provided
from .instance_normalizer import normalize_instance
from .type_decision_normalizer import normalize_type_decison
from .procedural_class_normalizer import normalize_procedural_class
from .data_normalizer import normalize_data
from .judgment_court_normalizer import normalize_judgment_court
from .reprocessed_normalizer import change_flag_reprocessed_to_true
from base_crawler.helper import save_item_to_database
from busca_transfromer.transformer.transformer_pipeline import _normalize_item
from busca_transfromer.teste import teste

class TransformerPipeline:
    database = "STG_outputs"

    def _normalize_item(self, item):
        transformed_item = normalize_rapporteur(item)
        transformed_item = normalize_area(transformed_item)
        transformed_item = normalize_instance(transformed_item)
        transformed_item = normalize_summary(transformed_item)
        transformed_item = normalize_provided(transformed_item)
        transformed_item = normalize_type_decison(transformed_item)
        transformed_item = normalize_procedural_class(transformed_item)
        transformed_item = normalize_data(transformed_item)
        transformed_item = normalize_judgment_court(transformed_item)
        transformed_item = change_flag_reprocessed_to_true(transformed_item)
        return transformed_item

    def _save_transformed_item_in_database(self, transformed_item, crawler_name,court_name):
        save_item_to_database(self.database, crawler_name, transformed_item,court_name)

    def process_item(self, item, spider):
        # try:
            teste()
            transformed_item = _normalize_item(item)
            court_name = transformed_item.get("data", {}).get("tribunal", "")
            collection_name = f"crawler-juris-{court_name}".casefold()
            self._save_transformed_item_in_database(transformed_item, collection_name,court_name)
            spider.logger.debug(
                f"Item {transformed_item} - sent to mongo database {self.database} - collection {collection_name}"
            )
            return transformed_item
        # except Exception as e:
        #     raise TransformerPipelineException(str(e))

