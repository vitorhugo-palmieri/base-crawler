import re

_TREATED_AREA_FIELD = "area"
_re_admin = re.compile(r"ADM", re.IGNORECASE)
_re_civel = re.compile(r"C[IÍ]V", re.IGNORECASE)
_re_criminal = re.compile(r"CRIM", re.IGNORECASE)
_re_trabalhista = re.compile(r"TRAB", re.IGNORECASE)
_re_tribut = re.compile(r"TRIB", re.IGNORECASE)

CIVIL = "CÍVEL"
TRIBUTARY = "TRIBUTÁRIO"
CRIMINAL = "PENAL"
ADMINISTRATIVE = "ADMINISTRATIVO / PÚBLICO"
ELECTORAL = "ELEITORAL"
PENSION = "PREVIDENCIÁRIO"
NOT_FOUND = "NÃO ENCONTRADO"
LABORITE = "TRABALHISTA"


def _get_area_from_jurisprudence_class(item):
    return item


def _normalize_area_field(item):
    treated_area = ""
    area_label = item.get("data", {}).get("area")
    if _re_admin.match(area_label) is not None:
        treated_area = ADMINISTRATIVE
    elif _re_civel.match(area_label) is not None:
        treated_area = CIVIL
    elif _re_criminal.match(area_label) is not None:
        treated_area = CRIMINAL
    elif _re_tribut.match(area_label) is not None:
        treated_area = TRIBUTARY
    else:
        treated_area = NOT_FOUND

    item["data"][_TREATED_AREA_FIELD] = treated_area
    return item


def _extract_area_in_summary(item):
    if not "ementa" in item["data"]:
        result = NOT_FOUND
    else:
        summary = item["data"]["ementa"]
        court = item["data"]["tribunal"]
        if court == "TST" or "TRT" in court:
            result = LABORITE
        elif court == "TSE" or "TRE" in court:
            result = ELECTORAL
        elif re.findall(r"PROCESS(UAL|O)\sPENAL", summary):
            result = CRIMINAL
        elif re.findall(r"RESPONSABILIDAD(E|ES)\sC[IÍ]VI(L|S)", summary):
            result = TRIBUTARY
        elif re.findall(r"D[IÍ]VID(A|AS)\sATIV(A|AS)", summary):
            result = TRIBUTARY
        elif re.findall(r"EXECUÇ(ÃO|ÕES)\sFISCA(L|IS)", summary):
            result = TRIBUTARY
        elif re.findall(r"DIREITO\sTRIBUT[AÁ]RIO", summary):
            result = TRIBUTARY
        elif re.findall(r"TRIBUTÁRIO", summary):
            result = TRIBUTARY
        elif re.findall(r"CONSTITUCIONAL", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"ADMINISTRATIVO", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"PENA(L|IS)", summary):
            result = CRIMINAL
        elif re.findall(r"PREVIDENCI[AÁ]RI(O|OS)", summary):
            result = PENSION
        elif re.findall(r"PREVID[EÊ]NCIA", summary):
            result = PENSION
        elif re.findall(r"EXECUTIV(O|OS)\sFISCA(L|IS)", summary):
            result = TRIBUTARY
        elif re.findall(r"TRIBUT(O|OS)", summary):
            result = TRIBUTARY
        elif re.findall(r"SERVI(DOR|DORES)\sPÚBLIC(O|OS)", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"FUNCIONALISMO\sPÚBLICO", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"FUNCION[AÁ]RI(O|OS)\sPÚBLIC(O|OS)", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"LICITAÇÕES\sE\sCONTRATOS", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"IMPROBIDADE\sADMINISTRATIVA", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"ATOS\ADMINISTRATIVOS", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"AGENTES\sPÚBLICOS", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"PAD", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"RESPONSABILIDADE\sC[IÍ]VIL\sDO\sESTADO", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"SERVIÇO\sPÚBLICO", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"ORGANIZAÇÃO\sADMINISTRATIVA", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"BENS\sPÚBLICOS", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"DESAPROPRIAÇÃO", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"PODERES\sADMINISTRATIVOS", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"ERRO\sADMINISTRATIVO", summary):
            result = ADMINISTRATIVE
        elif re.findall(r"AÇÃO\sCIVIL\sPÚBLICA", summary):
            result = ADMINISTRATIVE
        elif re.findall(
            r"AÇ(ÃO|ÕES)\sDIRET(A|AS)\sD(E|A)\sINCONSTITUCIONALIDADE", summary
        ):
            result = ADMINISTRATIVE
        elif re.findall(r"direito\stribut[AÁ]rio", summary, flags=re.IGNORECASE):
            result = TRIBUTARY
        elif re.findall(r"direit(o|os)\sc[IÍ]v(i|e)l", summary, flags=re.IGNORECASE):
            result = CIVIL
        elif re.findall(r"direit(o|os)\sp[UÚ]blico(s)", summary, flags=re.IGNORECASE):
            result = ADMINISTRATIVE
        elif re.findall(r"direit(o|os)\spena(l|is)", summary, flags=re.IGNORECASE):
            result = CRIMINAL
        elif re.findall(
            r"direit(o|os)\sconsumid(or|ores)", summary, flags=re.IGNORECASE
        ):
            result = CIVIL
        elif re.findall(
            r"direit(o|os)\sempresari(ais|al)", summary, flags=re.IGNORECASE
        ):
            result = CIVIL
        elif re.findall(r"direit(o|os)\stributari(o|os)", summary, flags=re.IGNORECASE):
            result = TRIBUTARY
        elif re.findall(r"direito\sadministrativo", summary, flags=re.IGNORECASE):
            result = ADMINISTRATIVE
        elif re.findall(r"direito\scriminal", summary, flags=re.IGNORECASE):
            result = CRIMINAL
        elif re.findall(r"direito\spenal", summary, flags=re.IGNORECASE):
            result = CRIMINAL
        elif re.findall(r"aç(ão|ões)\spena(l|is)", summary, flags=re.IGNORECASE):
            result = CRIMINAL
        elif re.findall(r"apelaç[AÃ]o\scriminal", summary, flags=re.IGNORECASE):
            result = CRIMINAL
        elif re.findall(r"apelaç[OÕ]es\scriminal", summary, flags=re.IGNORECASE):
            result = CRIMINAL
        elif re.findall(r"c[AÂ]mara\scriminal", summary, flags=re.IGNORECASE):
            result = CRIMINAL
        elif re.findall(r"constitucional", summary, flags=re.IGNORECASE):
            result = ADMINISTRATIVE
        elif re.findall(r"PROCESSUAL\sC[IÍ]VIL", summary, flags=re.IGNORECASE):
            result = CIVIL
        else:
            result = NOT_FOUND
    item["data"][_TREATED_AREA_FIELD] = result
    return item


def normalize_area(item):
    new_item = item.copy()
    enriched_item = _extract_area_in_summary(new_item)
    if (
        NOT_FOUND in enriched_item.get("data", {}).get(_TREATED_AREA_FIELD)
        and "area" in new_item["data"]
    ):
        return _normalize_area_field(new_item)
    return enriched_item
