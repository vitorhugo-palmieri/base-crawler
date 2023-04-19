import re


def _remove_tags_html(item):
    try:
        text_without_tags_html = re.sub("<[^>]+?>", "", item)
        return text_without_tags_html
    except:
        return ""


def _replace_extra_space(text):
    text = re.sub(r"\s +", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"^[\n]*EMENTA:?", "", text, flags=re.IGNORECASE)
    return text.strip()


def _normalize_summary_without_tags(summary):
    treated_summary = ""
    if summary is not None:
        treated_summary = _remove_tags_html(summary)
        treated_summary_without_extra_space = _replace_extra_space(treated_summary)
    return treated_summary_without_extra_space


def _normalize_summary_without_css_code(summary):
    treated_summary = ""
    if "@media" in summary:
        treated_summary = summary.split("#fafafa;\n\t}")[1]
    summary = treated_summary
    return _normalize_summary_without_tags(summary)


def _call_functions(new_item):
    if "@media" in new_item:
        return _normalize_summary_without_css_code(new_item)
    return _normalize_summary_without_tags(new_item)


def _remove_break_lines(summary):
    return re.sub(r"\n", " ", summary)


def normalize_summary(item):

    ementa = item.get("data", {}).get("ementa", "")
    inteiroTeorTexto = item.get("data", {}).get("inteiroTeorTexto", "")

    new_item = item.copy()

    if ementa.isnumeric():
        if new_item.get("data", {}).get("ementaSemFormatacao"):
            ementa = new_item.get("data", {}).get("ementaSemFormatacao")
            del new_item["data"]["ementaSemFormatacao"]

    if new_item.get("data", {}).get("ementaSemFormatacao"):
        del new_item["data"]["ementaSemFormatacao"]

    if (ementa == "") and (inteiroTeorTexto == ""):
        return item

    if ementa == inteiroTeorTexto:
        del new_item["data"]["ementa"]
        ementa = ""

    if ementa:
        #if item.get("data").get("tribunal") == "TJPR":
        ementa = _remove_break_lines(ementa)

        summary = _call_functions(ementa)
        if summary == "":
            del new_item["data"]["ementa"]
        else:
            new_item["data"]["ementa"] = summary

    if inteiroTeorTexto:
        new_item["data"]["inteiroTeorTexto"] = _call_functions(inteiroTeorTexto)

    return new_item
