import re
from re import IGNORECASE
from .utils_judgment_court import WRONG_LIST


def replace_ordinal(item):
    return item.replace("ª", "a").replace("º", "o").replace("°", "o")


def replace_cadeira(text):
    return re.sub("-\scadeira\s+\d+", "", text, flags=IGNORECASE).strip()


def is_word_exists_in_text(word, text):
    return word in text


def _sanitized_filter_judgment_court(item):

    judgment_court = item.get("data", {}).get("orgaoJulgador")
    judgment_court = replace_cadeira(judgment_court)
    judgment_court = judgment_court.lower()

    for key, value in reversed(WRONG_LIST.items()):
        key = key.lower()
        if is_word_exists_in_text(key, judgment_court):
            judgment_court = judgment_court.replace(key, value)

    judgment_court = replace_ordinal(judgment_court)

    item["data"]["orgaoJulgador"] = judgment_court

    return item


def normalize_judgment_court(item):
    judgment_court = item.get("data", {}).get("orgaoJulgador")
    if judgment_court is None:
        return item
    new_item = item.copy()
    return _sanitized_filter_judgment_court(new_item)
