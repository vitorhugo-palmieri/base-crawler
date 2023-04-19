import unicodedata
from base64 import decode
from .utils_procedural_class import (
    CLASSES_FOR_SANITIZED_CLASSES,
    SANITIZED_CLASSES_TO_FILTER_CLASSES,
)

_TREATED_PROCEDURAL_CLASS_FIELD = "classeProcessual"
_FILTER_PROCEDURAL_CLASS_FIELD = "classeProcessualFilter"


def _get_area_from_jurisprudence_class(item):
    return item


def _verify_procedural_class_and_fix_name(item):
    list_wrongs_procedural_class = ["classProcessual", "classe"]
    if "classeProcessual" in item["data"]:
        return item
    for procedural_class in list_wrongs_procedural_class:
        if procedural_class in item["data"]:
            item["data"]["classeProcessual"] = item["data"][procedural_class]
            del item["data"][procedural_class]
            return item
    else:
        return None


def _remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    only_ascii = nfkd_form.encode("ASCII", "ignore")
    return only_ascii.decode("utf-8")


def _sanitized_procedural_class(item):
    proceduralClass_ = _verify_procedural_class_and_fix_name(item)
    proceduralClass = _remove_accents(
        proceduralClass_["data"].get("classeProcessual").upper()
    )
    for key, value in CLASSES_FOR_SANITIZED_CLASSES.items():
        if proceduralClass == _remove_accents(key.upper()):
            item["data"][_TREATED_PROCEDURAL_CLASS_FIELD] = value
            return item
    else:
        item["data"][_TREATED_PROCEDURAL_CLASS_FIELD] = proceduralClass.upper()
        return item


def _sanitized_filter_procedural_class(item):
    if not _TREATED_PROCEDURAL_CLASS_FIELD in item["data"]:
        return item
    procedural_class_to_filter = item["data"][_TREATED_PROCEDURAL_CLASS_FIELD]
    for key, value in SANITIZED_CLASSES_TO_FILTER_CLASSES.items():
        if procedural_class_to_filter == key:
            item["data"][_FILTER_PROCEDURAL_CLASS_FIELD] = value.upper()
            return item
    else:
        return item


def _long_name(item):
    if len(item["data"]["classeProcessual"]) > 200:
        return True


def normalize_procedural_class(item):

    if _verify_procedural_class_and_fix_name(item) is None:
        return _get_area_from_jurisprudence_class(item)
    new_item = item.copy()

    if _long_name(new_item):
        new_item["data"]["classeProcessual"] = ""
        return new_item

    item_enrich = _sanitized_procedural_class(new_item)
    item_enrich = _sanitized_filter_procedural_class(item_enrich)
    return item_enrich
