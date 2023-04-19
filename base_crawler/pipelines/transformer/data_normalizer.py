from datetime import datetime
import re

_re_find_date = re.compile(r"(\d{2}-\d{2}-\d{2})")
_re_find_date_wrong = re.compile(r"(\d{3}-\d{2}-\d{2})")


def _get_area_from_jurisprudence_class(item):
    return item


def _enrich_date_index_field(item):
    new_item = _normalizer_data(item)
    if new_item["data"].get("dataPublicacao") is not None:
        new_item["data"]["dataIndexacao"] = new_item["data"]["dataPublicacao"]
        return new_item
    elif new_item["data"].get("dataJulgamento") is not None:
        new_item["data"]["dataIndexacao"] = new_item["data"]["dataJulgamento"]
        return new_item
    else:
        return None


def _convert_wrong_iso_to_correctly_iso(date):
    return datetime.strftime(datetime.strptime(date, "%y-%m-%d"), "%Y-%m-%d")


def convert_date_from_br_to_iso(date_string):
    if not validate_date_format(date_string, "%d-%m-%Y"):
        return None
    return datetime.strftime(datetime.strptime(date_string, "%d-%m-%Y"), "%Y-%m-%d")


def validate_date_format(date_string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except:
        return False


def _find_date(date):
    return _re_find_date.search(date).group(1)


def _find_date_wrong(date):
    return _re_find_date_wrong.search(date).group(1)


def _normalizer_data(item):
    new_item = item.copy()

    if new_item["data"].get("dataPublicacao") is not None and validate_date_format(
        new_item["data"].get("dataPublicacao"), "%d-%m-%Y"
    ):
        new_item["data"]["dataPublicacao"] = convert_date_from_br_to_iso(
            new_item["data"].get("dataPublicacao")
        )
        return new_item
    elif new_item["data"].get("dataJulgamento") is not None and validate_date_format(
        new_item["data"].get("dataJulgamento"), "%d-%m-%Y"
    ):
        new_item["data"]["dataJulgamento"] = convert_date_from_br_to_iso(
            new_item["data"].get("dataJulgamento")
        )
        return new_item
    if new_item["data"].get("dataPublicacao") is not None and new_item["data"].get(
        "dataPublicacao"
    ) == _find_date(new_item["data"].get("dataPublicacao")):
        new_item["data"]["dataPublicacao"] = _convert_wrong_iso_to_correctly_iso(
            new_item["data"].get("dataPublicacao")
        )
        return new_item
    elif new_item["data"].get("dataPublicacao") is not None and new_item["data"].get(
        "dataPublicacao"
    ) == _find_date_wrong(new_item["data"].get("dataPublicacao")):
        del new_item["data"]["dataPublicacao"]
        return new_item
    elif new_item["data"].get("dataJulgamento") is not None and new_item["data"].get(
        "dataJulgamento"
    ) == _find_date(new_item["data"].get("dataJulgamento")):
        new_item["data"]["dataJulgamento"] = _convert_wrong_iso_to_correctly_iso(
            new_item["data"].get("dataJulgamento")
        )
        return new_item
    elif new_item["data"].get("dataJulgamento") is not None and new_item["data"].get(
        "dataJulgamento"
    ) == _find_date_wrong(new_item["data"].get("dataJulgamento")):
        del new_item["data"]["dataJulgamento"]
        return new_item
    else:
        return item


def normalize_data(item):
    try:
        if _enrich_date_index_field(item) is None:
            return _get_area_from_jurisprudence_class(item)
        new_item = item.copy()
        return _enrich_date_index_field(new_item)
    except Exception as e:
        print(f"Error in data {e} ---- item {item}")
