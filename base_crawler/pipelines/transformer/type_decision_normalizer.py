import re
import unicodedata

_TREATED_DECISION_FIELD = "tipoDecisao"

ACCORDION = "ACÓRDÃO"
MONOCRATIC_DECISION = "DECISÃO MONOCRÁTICA"
DISPATCH = "DESPACHO"
SUMULA = "SÚMULA"
BINDING_PRECEDENT = "SÚMULA VINCULANTE"
JUDGMENT = "SENTENÇA"
RESOLUTION = "RESOLUÇÃO"
INTERLOCUTORY_DECISION = "DECISÃO INTERLOCUTÓRIA"


def _get_from_jurisprudence_class(item):
    return item


def _normalize_type_decision(item):
    document_type = item["data"]["tipoDecisao"]
    if re.findall(r"Ac[OÓ]rd[AÃ]o", document_type, flags=re.IGNORECASE):
        treated_document_type = ACCORDION
    elif (
        re.findall(r"decis(ao|ão)", document_type, flags=re.IGNORECASE)
        and item["data"].get("instancia", "") == 1
    ):
        treated_document_type = INTERLOCUTORY_DECISION
    elif re.findall(r"monocr[AÁ]tica", document_type, flags=re.IGNORECASE):
        treated_document_type = MONOCRATIC_DECISION
    elif re.findall(r"decisão", document_type, flags=re.IGNORECASE):
        treated_document_type = MONOCRATIC_DECISION
    elif re.findall(r"mono", document_type, flags=re.IGNORECASE):
        treated_document_type = MONOCRATIC_DECISION
    elif re.findall(r"sumula(s) vinculantes", document_type, flags=re.IGNORECASE):
        treated_document_type = BINDING_PRECEDENT
    elif re.findall(r"sumula(s)", document_type, flags=re.IGNORECASE):
        treated_document_type = SUMULA
    elif re.findall(r"senten(c|ç)(a|as)", document_type, flags=re.IGNORECASE):
        treated_document_type = JUDGMENT
    elif re.findall(r"resolu(c|ç)(ão|ao)", document_type, flags=re.IGNORECASE):
        treated_document_type = RESOLUTION
    else:
        treated_document_type = document_type

    item["data"][_TREATED_DECISION_FIELD] = treated_document_type.upper()
    return item


def normalize_type_decison(item):
    if item["data"].get("tipoDecisao") is None:
        return _get_from_jurisprudence_class(item)
    new_item = item.copy()
    return _normalize_type_decision(new_item)
