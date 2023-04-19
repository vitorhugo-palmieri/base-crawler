import re

"""
## README ##

If you do not have the "reporter" field in the input, the input is delivered without treatment.
If you do not have the "tipoDecisao" field in the input, it will be treated as an agreement.

VARIABLES:
-- _re_des_fed_min --
Exceptions and patterns that will be deleted from the reporting field coming from the input, before applying treatment.

-- _other_decisions --
Types of decisions that will be dealt with by the JUDGE in the reporting field.

"""

_re_trat = re.compile(
    r"|JU[IÍ]ZA?|FEDERAL|DESEMBARGADORA?|DESª.?|DES\.\(A\)|\(A\).?|\bDES\b\.?|MINISTR[OA]|\bMIN\b\.?|\(PRESIDENTE TRIBUNAL DE JUSTIÇA\)|P[ORT]*[ARIA]*\s*[Nº]*\s*[\d]+[/\d+]*|-|\(PRES. DA SEÇÃO DE DIREITO PÚBLICO\)",
    flags=re.IGNORECASE,
)
_special_decisions = re.compile(
    r"SENTEN[CÇ]A|DECIS[AÃ]O[_ ]INTERLOCUT[OÓ]RIAS?", flags=re.IGNORECASE
)
_re_judge_summoned = re.compile(r"CONVOCAD[OA]|CONV.", flags=re.IGNORECASE)
_re_judge_summoned_des = re.compile(r"DESEMBARGADORA?|\bDES\b", flags=re.IGNORECASE)
_re_judge_summoned_min = re.compile(r"MINISTRO?|\bMIN\b", flags=re.IGNORECASE)
_TREATED_RAPPORTEUR_FIELD = "relator"


def _normalize_superior(item, decision):
    item["data"][_TREATED_RAPPORTEUR_FIELD] = "MIN. " + item["data"]["relator"]
    return item


def _normalize_federal(item, decision):

    if re.findall(_special_decisions, decision):
        item["data"][_TREATED_RAPPORTEUR_FIELD] = (
            "JUIZ(a) FED. " + item["data"]["relator"]
        )
    else:
        item["data"][_TREATED_RAPPORTEUR_FIELD] = "DES. FED. " + item["data"]["relator"]
    return item


def _normalize_state(item, decision):

    if re.findall(_special_decisions, decision):
        item["data"][_TREATED_RAPPORTEUR_FIELD] = "JUIZ(a) " + item["data"]["relator"]
    else:
        item["data"][_TREATED_RAPPORTEUR_FIELD] = "DES. " + item["data"]["relator"]
    return item


def _clean_before_normalize(item):
    item["data"]["relator"] = _re_trat.sub("", item["data"]["relator"]).strip()
    return item


def _judge_summoned(item):
    rapporteur = item["data"]["relator"]
    item["data"]["relator"] = re.sub(
        r"FEDERAL", "FED.", rapporteur, flags=re.IGNORECASE
    )
    if re.findall(r"JU[IÍ]ZA?", rapporteur, flags=re.IGNORECASE):
        item = _clean_before_normalize(item)
        item["data"][_TREATED_RAPPORTEUR_FIELD] = "JUIZ(a) " + item["data"]["relator"]
    elif re.findall(_re_judge_summoned_des, rapporteur):
        item = _clean_before_normalize(item)
        item["data"][_TREATED_RAPPORTEUR_FIELD] = "DES. " + item["data"]["relator"]
    elif re.findall(_re_judge_summoned_min, rapporteur):
        item = _clean_before_normalize(item)
        item["data"][_TREATED_RAPPORTEUR_FIELD] = "MIN. " + item["data"]["relator"]
    else:
        item = _clean_before_normalize(item)
        item["data"][_TREATED_RAPPORTEUR_FIELD] = "JUIZ(a) " + item["data"]["relator"]
    return item


def _long_name(item):
    if len(item["data"]["relator"]) > 100:
        return True


def normalize_rapporteur(item):

    if item["data"].get("relator") is None:
        return item

    if item["data"].get("tipoDecisao") is None:
        decision = "ACORDÃO"
    else:
        decision = item["data"].get("tipoDecisao")

    new_item = item.copy()

    if _long_name(new_item):
        new_item["data"][_TREATED_RAPPORTEUR_FIELD] = ""
        return new_item

    if re.findall(_re_judge_summoned, new_item["data"]["relator"]):
        return _judge_summoned(new_item)

    new_item = _clean_before_normalize(new_item)

    if new_item["data"]["tribunal"].startswith("TRF"):
        return _normalize_federal(new_item, decision)
    if new_item["data"]["tribunal"].startswith("ST") or new_item["data"][
        "tribunal"
    ].startswith("TS"):
        return _normalize_superior(new_item, decision)
    return _normalize_state(new_item, decision)
