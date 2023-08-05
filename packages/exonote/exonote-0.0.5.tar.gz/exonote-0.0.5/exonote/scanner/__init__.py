import oscan
from exonote import dto
from exonote.element import Element
from exonote.pattern import Pattern
from exonote.error import Error


def scan(text):
    cached_string = ""
    for token in oscan.scan(text, Pattern):
        element, data = _read_token(token)
        if element == Element.STRING:
            cached_string += data["text"]
        else:
            if cached_string:
                yield dto.Token(Element.STRING, {"text": cached_string})
                cached_string = ""
            yield dto.Token(element, data)
    if cached_string:
        yield dto.Token(Element.STRING, {"text": cached_string})


def _read_token(token):
    updaters = {Pattern.ANCHOR_1.name: _update_anchor_data,
                Pattern.ATTACHMENT_1.name: _update_attachment_data,
                Pattern.ATTACHMENT_2.name: _update_attachment_data,
                Pattern.BOLD_1.name: _update_bold_data,
                Pattern.CODE_1.name: _update_code_data,
                Pattern.CODEBLOCK_1.name: _update_codeblock_data,
                Pattern.DINKUS_1.name: _update_dinkus_data,
                Pattern.GAP_1.name: _update_gap_data,
                Pattern.HEADING_1.name: _update_heading_data,
                Pattern.ITALIC_1.name: _update_italic_data,
                Pattern.ITEM_1.name: _update_item_data,
                Pattern.LINK_1.name: _update_link_data,
                Pattern.LINK_2.name: _update_link_data,
                Pattern.MONOSPACE_1.name: _update_monospace_data,
                Pattern.NOTICE_1.name: _update_notice_data,
                Pattern.PROGRAM_1.name: _update_program_data,
                Pattern.PROGRAM_2.name: _update_program_data,
                Pattern.STRIKETHROUGH_1.name: _update_strikethrough_data,
                Pattern.STRING_1.name: _update_string_data,
                Pattern.TABLE_1.name: _update_table_data,
                Pattern.UNDERLINE_1.name: _update_underline_data,
                Pattern.VARIABLE_1.name: _update_variable_data,
                Pattern.WARNING_1.name: _update_warning_data}
    try:
        updater = updaters[token.name]
    except KeyError as e:
        raise Error("Unknown pattern {} !".format(token.name)) from None
    else:
        data = _get_regex_data(token)
        updater(data)
    element = _get_element(token.name)
    return element, data


def _get_element(pattern):
    mapping = {Pattern.ANCHOR_1.name: Element.ANCHOR,
               Pattern.ATTACHMENT_1.name: Element.ATTACHMENT,
               Pattern.ATTACHMENT_2.name: Element.ATTACHMENT,
               Pattern.BOLD_1.name: Element.BOLD,
               Pattern.CODE_1.name: Element.CODE,
               Pattern.CODEBLOCK_1.name: Element.CODEBLOCK,
               Pattern.DINKUS_1.name: Element.DINKUS,
               Pattern.GAP_1.name: Element.GAP,
               Pattern.HEADING_1.name: Element.HEADING,
               Pattern.ITALIC_1.name: Element.ITALIC,
               Pattern.ITEM_1.name: Element.ITEM,
               Pattern.LINK_1.name: Element.LINK,
               Pattern.LINK_2.name: Element.LINK,
               Pattern.MONOSPACE_1.name: Element.MONOSPACE,
               Pattern.NOTICE_1.name: Element.NOTICE,
               Pattern.PROGRAM_1.name: Element.PROGRAM,
               Pattern.PROGRAM_2.name: Element.PROGRAM,
               Pattern.STRIKETHROUGH_1.name: Element.STRIKETHROUGH,
               Pattern.STRING_1.name: Element.STRING,
               Pattern.TABLE_1.name: Element.TABLE,
               Pattern.UNDERLINE_1.name: Element.UNDERLINE,
               Pattern.VARIABLE_1.name: Element.VARIABLE,
               Pattern.WARNING_1.name: Element.WARNING}
    try:
        element = mapping[pattern]
    except KeyError as e:
        raise Error("Unknown pattern {} !".format(pattern)) from None
    return element


def _get_regex_data(token):
    data = dict()
    for key, val in token.groups_dict.items():
        cache = key.split("_", maxsplit=1)
        item = cache[1]
        data[item] = val
    return data


def _update_anchor_data(data):
    pass


def _update_attachment_data(data):
    if not data.get("title") and not data.get("variable"):
        data["title"] = data.get("target")
    caption = data.get("caption")
    three_dots = "..."
    if caption and caption.strip() == three_dots:
        data["caption"] = three_dots


def _update_bold_data(data):
    text = data.get("text", "")
    text = text.replace("\\*", "*")
    text = text.replace("\n", " ")
    data["text"] = text


def _update_code_data(data):
    text = data.get("text", "")
    text = text.replace("\\`", "`")
    text = text.replace("\n", " ")
    data["text"] = text


def _update_codeblock_data(data):
    pass


def _update_dinkus_data(data):
    pass


def _update_gap_data(data):
    pass


def _update_heading_data(data):
    level = len(data["level"])
    data["level"] = level
    text = data.get("text", "")
    data["text"] = text.strip()
    sid = data.get("id", "")
    if not sid:
        data["id"] = text.replace(" ", "_")
    data["id"] = "<{}>".format(data["id"].lower())
    alignment = data.get("center", "")
    data["center"] = True if alignment else False


def _update_italic_data(data):
    text = data.get("text", "")
    text = text.replace("\\_", "_")
    text = text.replace("\n", " ")
    data["text"] = text


def _update_item_data(data):
    pass


def _update_link_data(data):
    data["executable"] = False
    command = data.get("command")
    if command:
        data["executable"] = True
        data["target"] = command
    if not data.get("text") and not data.get("variable"):
        data["text"] = data.get("target")


def _update_monospace_data(data):
    text = data.get("text", "")
    text = text.replace("\\`", "`")
    text = text.replace("\n", " ")
    data["text"] = text


def _update_notice_data(data):
    text = data.get("text", "")
    text = text.replace("\\!", "!")
    text = text.replace("\n", " ")
    data["text"] = text


def _update_program_data(data):
    command = data.get("command", "")
    data["command"] = command.strip("{}")


def _update_strikethrough_data(data):
    text = data.get("text", "")
    text = text.replace("\\~", "~")
    text = text.replace("\n", " ")
    data["text"] = text


def _update_string_data(data):
    text = data.get("text", "")
    text = text.replace("\\`", "`")
    text = text.replace("\\*", "*")
    text = text.replace("\\_", "_")
    text = text.replace("\\!", "!")
    text = text.replace("\\~", "~")
    text = text.replace("\n", " ")
    data["text"] = text


def _update_table_data(data):
    caption = data.get("caption")
    three_dots = "..."
    if caption and caption.strip() == three_dots:
        data["caption"] = three_dots


def _update_underline_data(data):
    text = data.get("text", "")
    data["text"] = text.replace("\\_", "_")


def _update_variable_data(data):
    value = data.get("value", "")
    data["value"] = value.strip()


def _update_warning_data(data):
    text = data.get("text", "")
    data["text"] = text.replace("\\!", "!")
