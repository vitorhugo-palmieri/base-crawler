import re

_re_find_only_number_instance = re.compile(r"(\d+)")


def _add_field_instance(new_item):
    instance = ""
    type_decision = new_item.get("data", {}).get("tipoDecisao", "")
    if new_item["data"]["tribunal"] == "STF":
        instance = 4
    elif new_item["data"]["tribunal"].startswith("ST") or new_item["data"][
        "tribunal"
    ].startswith("TS"):
        instance = 3
    elif type_decision == "sentenca" or type_decision == "decisao_interlocutoria":
        instance = 1
    else:
        instance = 2
    new_item["data"]["instancia"] = instance
    return new_item


def _normalize_instance(new_item):
    instance = new_item.get("data", {}).get("instancia", "")
    instance_only_number = _re_find_only_number_instance.search(str(instance)).group(1)
    new_item["data"]["instancia"] = int(instance_only_number)
    return new_item


def normalize_instance(item):
    new_item = item.copy()
    if new_item.get("data", {}).get("instancia") is not None:
        return _normalize_instance(new_item)
    item_with_instance = _add_field_instance(new_item)
    return _normalize_instance(item_with_instance)
