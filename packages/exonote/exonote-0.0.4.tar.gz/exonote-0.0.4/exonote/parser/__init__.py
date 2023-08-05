from exonote.scanner import scan
from exonote.element import Element


def parse(text):
    """parse a text"""
    structure = list()
    variables = dict()
    for token in scan(text):
        if token.element == Element.VARIABLE:
            name, value = token.data["name"], token.data["value"]
            variables[name] = value
            continue
        cache = (token.element, token.data)
        structure.append(cache)
    _update_structure(structure, variables)
    return structure


def _update_structure(structure, variables):
    mapping = {Element.ATTACHMENT: _update_attachment,
               Element.PROGRAM: _update_program,
               Element.LINK: _update_link}
    for element, data in structure:
        if element not in mapping:
            continue
        updater = mapping.get(element)
        updater(data, variables)


def _update_attachment(data, variables):
    name = data.get("variable")
    if not name:
        return
    value = variables.get(name, "")
    data["target"] = value
    if not data.get("title"):
        data["title"] = value


def _update_program(data, variables):
    value = data.get("variable")
    if not value:
        return
    value = variables.get(value, "")
    data["command"] = value.strip().strip("{}")


def _update_link(data, variables):
    name = data.get("variable")
    if not name:
        return
    value = variables.get(name, "")
    target = value.strip()
    data["executable"] = False
    if target.startswith("{") and target.endswith("}"):
        data["executable"] = True
        target = value.strip("{}")
    data["target"] = target
    if not data.get("text"):
        data["text"] = target
