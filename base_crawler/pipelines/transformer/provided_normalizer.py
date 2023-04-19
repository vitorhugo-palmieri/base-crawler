import re

_TREATED_PROVIDED_FIELD = "provimento"

NOT_FOUND = "NÃO ENCONTRADO"
PROVIDED = "PROVIDO"
NOT_PROVIVED = "NÃO PROVIDO"
PARTIALLY_PROVIVED = "PARCIALMENTE PROVIDO"


def _find_provided(item):
    if not "ementa" in item["data"]:
        result = NOT_FOUND
    else:
        summary = item["data"]["ementa"]
        if re.findall(r"parcialmente\sprovido", summary, flags=re.IGNORECASE):
            result = PARTIALLY_PROVIVED
        elif re.findall(r"parcialmente\sprocedente", summary, flags=re.IGNORECASE):
            result = PARTIALLY_PROVIVED
        elif re.findall(r"parcialmente\sprovid(o|a)", summary, flags=re.IGNORECASE):
            result = PARTIALLY_PROVIVED
        elif re.findall(r"parcialmente\sprovid(o|os)", summary, flags=re.IGNORECASE):
            result = PARTIALLY_PROVIVED
        elif re.findall(r"proviment(o|os)\sparcial", summary, flags=re.IGNORECASE):
            result = PARTIALLY_PROVIVED
        elif re.findall(r"parcial\sproviment(o|os)", summary, flags=re.IGNORECASE):
            result = PARTIALLY_PROVIVED
        elif re.findall(r"parcialmente\so\sac[OÓ]rdão", summary, flags=re.IGNORECASE):
            result = PARTIALLY_PROVIVED
        elif re.findall(r"providos? em partes?", summary, flags=re.IGNORECASE):
            result = PARTIALLY_PROVIVED
        elif re.findall(r"julgo(?:\s\w+){,3}\s?provido", summary, flags=re.IGNORECASE):
            result = PROVIDED
        elif re.findall(r"julgad(o|a)\sprocedente", summary, flags=re.IGNORECASE):
            result = PROVIDED
        elif re.findall(r"se\sd[AÁ]\sproviment(o|os)", summary, flags=re.IGNORECASE):
            result = PROVIDED
        elif re.findall(r"recurs(o|os)\sprovid(o|os)", summary, flags=re.IGNORECASE):
            result = PROVIDED
        elif re.findall(r"deu\sproviment(o|os)", summary, flags=re.IGNORECASE):
            result = PROVIDED
        elif re.findall(r"embargos\sacolhidos", summary, flags=re.IGNORECASE):
            result = PROVIDED
        elif re.findall(
            r"julgo(?:\s\w+){,3}\s?procedente", summary, flags=re.IGNORECASE
        ):
            result = PROVIDED
        elif re.findall(r"acolho\s(o|os)\spedido", summary, flags=re.IGNORECASE):
            result = PROVIDED
        elif re.findall(r"apelaç[AÃ]o\sacolhid(a|o)", summary, flags=re.IGNORECASE):
            result = PROVIDED
        elif re.findall(
            r"apelaç[OÕ]es\sacolhid(a|o)(as|os)", summary, flags=re.IGNORECASE
        ):
            result = PROVIDED
        elif re.findall(r"recurso\sacolhid(a|o)(as|os)", summary, flags=re.IGNORECASE):
            result = PROVIDED
        elif re.findall(
            r"acolh(o|emos)\sparcialmente\s(o|os)\spedido", summary, flags=re.IGNORECASE
        ):
            result = PARTIALLY_PROVIVED
        elif re.findall(
            r"acolh(o|emos)\s?em\s?parte\s?(o|os)\spedido", summary, flags=re.IGNORECASE
        ):
            result = PARTIALLY_PROVIVED
        elif re.findall(r"negado\sprovimento", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(
            r"apelaç(ão|ões)\srejeit(a|o)(as|os)", summary, flags=re.IGNORECASE
        ):
            result = NOT_PROVIVED
        elif re.findall(
            r"embarg(o|os)\sdeclaratóri(o|os)\srejeitad(o|os)",
            summary,
            flags=re.IGNORECASE,
        ):
            result = NOT_PROVIVED
        elif re.findall(
            r"embarg(o|os)\sde\sdeclaraç(ão|ões)\srejeitad(o|os)",
            summary,
            flags=re.IGNORECASE,
        ):
            result = NOT_PROVIVED
        elif re.findall(
            r"embarg(o|os)\sde\sinfrigênci(a|as)\srejeitad(o|os)",
            summary,
            flags=re.IGNORECASE,
        ):
            result = NOT_PROVIVED
        elif re.findall(
            r"embarg(o|os)\sde\sdivergênci(a|as)\srejeitad(o|os)",
            summary,
            flags=re.IGNORECASE,
        ):
            result = NOT_PROVIVED
        elif re.findall(r"embarg(o|os)\srejeitad(o|os)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"recurs(o|os)\srejeitad(o|os)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(
            r"nego\sseguiment(o|os)\sa(o|os)\srecurs(o|os)",
            summary,
            flags=re.IGNORECASE,
        ):
            result = NOT_PROVIVED
        elif re.findall(
            r"nego\sseguiment(o|os)\sa(o|os)\sapel(o|os)", summary, flags=re.IGNORECASE
        ):
            result = NOT_PROVIVED
        elif re.findall(
            r"nego\sseguiment(o|os)\sa(o|os)\sagrav(o|os)", summary, flags=re.IGNORECASE
        ):
            result = NOT_PROVIVED
        elif re.findall(
            r"nego\sseguiment(o|os)\sa(o|os)\sembarg(o|os)",
            summary,
            flags=re.IGNORECASE,
        ):
            result = NOT_PROVIVED
        elif re.findall(
            r"desfavor\sda\sparte\srecorrente", summary, flags=re.IGNORECASE
        ):
            result = NOT_PROVIVED
        elif re.findall(
            r"desfavor[AÁ]vel\sa\sparte\sautora", summary, flags=re.IGNORECASE
        ):
            result = NOT_PROVIVED
        elif re.findall(r"sentença\smantida", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"desprovid(o|os)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"apelação/sdesprovid(a|as)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"neg(o|a)/sprovimento", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"negou/sproviment(o|os)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"provimento/snegado", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"não\sprovid(o|a)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"não\sprovid(os|as)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"não\sprovimento\sao\srecurso", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"improvid(os|as)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"improvid(o|a)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(
            r"apela(ão|ões)\sdesprovid(a|as)", summary, flags=re.IGNORECASE
        ):
            result = NOT_PROVIVED
        elif re.findall(
            r"rejeito\s(?:o|os)\s(?:pedido|presente)", summary, flags=re.IGNORECASE
        ):
            result = NOT_PROVIVED
        elif re.findall(r"recurso\sprejudicad(o|a)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"apelo\sprejudicad(o|a)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"restou\sprejudicad(o|a)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(
            r"considerad(o|a)\sprejudicad(o|a)", summary, flags=re.IGNORECASE
        ):
            result = NOT_PROVIVED
        elif re.findall(r"julgo\sprejudicad(o|a)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"orde(m|ns) denegad(a|as)", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"negar provimento", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(r"nega-se\sprovimento", summary, flags=re.IGNORECASE):
            result = NOT_PROVIVED
        elif re.findall(
            r"provid(o|os)", summary, flags=re.IGNORECASE
        ):  ##EM último CASO
            result = PROVIDED
        else:
            result = NOT_FOUND

    item["data"][_TREATED_PROVIDED_FIELD] = result
    return item


def normalize_provided(item):
    new_item = item.copy()
    return _find_provided(new_item)
