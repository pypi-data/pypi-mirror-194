from enum import Enum


#  TODO: improve the regexes for these elements: emphasis (italic, etc), and links !

class Pattern(Enum):
    # top_gap, title, text, bottom_gap
    CODEBLOCK_1 = r"(?P<codeblock1_top_gap>\s*)^`{3}(?P<codeblock1_title>[^\s]*)(\r\n|\r|\n)(?P<codeblock1_text>[\s\S]*?)(\r\n|\r|\n)`{3}(?P<codeblock1_bottom_gap>\s*)"

    # top_gap, rows, caption, bottom_gap
    TABLE_1 = r"(?P<table1_top_gap>\s*)(?P<table1_rows>(?:\|.+?$(\r\n|\r|\n))+\|.*)(\r\n|\r|\n)(& (?P<table1_caption>.*)|)(?P<table1_bottom_gap>\s*)"

    # name, value
    VARIABLE_1 = r"^\[(?P<variable1_name>[\S]+)\] (?P<variable1_value>.*)(\r\n|\r|\n)?"
    
    # top_gap, level, alignment, text, id, bottom_gap
    HEADING_1 = r"(?P<heading1_top_gap>\s*)^(?P<heading1_level>#{1,6})(?P<heading1_center>(\.)?) (?P<heading1_text>.+?)([\s]+<(?P<heading1_id>[^\s]+)>|)[^\S\r\n]*$(?P<heading1_bottom_gap>\s*)"

    # top_gap, bottom_gap
    DINKUS_1 = r"(?P<dinkus1_top_gap>\s*)^[*]{3}(?P<dinkus1_bottom_gap>\s*)"

    # top_gap, title, target, variable, caption, bottom_gap
    ATTACHMENT_1 = r"(?P<attachment1_top_gap>\s*)^@\[(?P<attachment1_title>([^\s].*?[^\s]|))\](\((?P<attachment1_target>[^\s]*?)\)|\[(?P<attachment1_variable>[^\s]*?)\])(\r\n|\r|\n)& (?P<attachment1_caption>.+)$(?P<attachment1_bottom_gap>\s*)"
    
    # title, target, variable
    ATTACHMENT_2 = r"@\[(?P<attachment2_title>([^\s].*?[^\s]|))\](\((?P<attachment2_target>[^\s]*?)\)|\[(?P<attachment2_variable>[^\s]*?)\])"

    # top_gap, command, variable, caption, bottom_gap
    PROGRAM_1 = r"(?P<program1_top_gap>\s*)^\$({(?P<program1_command>[^\s].*?(?<!\\|\s))}|\[(?P<program1_variable>[^\s]*?)\])(\r\n|\r|\n)& (?P<program1_caption>.+)$(?P<program1_bottom_gap>\s*)"

    # command, variable
    PROGRAM_2 = r"\$({(?P<program2_command>[^\s].*?(?<!\\|\s))}|\[(?P<program2_variable>[^\s]*?)\])"
    
    # text, command, variable
    LINK_1 = r"\[(?P<link1_text>([^\s].*?[^\s]|))\](\({(?P<link1_command>[^\s].*?(?<!\\|\s))}\)|\[(?P<link1_variable>[^\s]*?)\])"
    
    # text, target, variable
    LINK_2 = r"\[(?P<link2_text>([^\s].*?[^\s]|))\](\((?P<link2_target>[^\s]*?)(?<!\\)\)|\[(?P<link2_variable>[^\s]*?)\])"
    
    # text
    CODE_1 = r"(?<!\\)(``(?P<code1_text>[^\s](?:.+?(\r\n|\r|\n)?)*?(?<!\\|\s))``)"

    # text
    MONOSPACE_1 = r"(?<!\\)(`(?P<monospace1_text>[^\s](?:.+?(\r\n|\r|\n)?)*?(?<!\\|\s))`)"

    # text
    BOLD_1 = r"(?<!\\)(\*(?P<bold1_text>[^\s](?:.+?(\r\n|\r|\n)?)*?(?<!\\|\s))\*)"

    # text
    UNDERLINE_1 = r"(?<!\\)(__(?P<underline1_text>[^\s](?:.+?(\r\n|\r|\n)?)*?(?<!\\|\s))__)"

    # text
    ITALIC_1 = r"(?<!\\)(_(?P<italic1_text>[^\s](?:.+?(\r\n|\r|\n)?)*?(?<!\\|\s))_)"

    # text
    WARNING_1 = r"(?<!\\)(%%(?P<warning1_text>[^\s](?:.+?(\r\n|\r|\n)?)*?(?<!\\|\s))%%)"

    # text
    NOTICE_1 = r"(?<!\\)(%(?P<notice1_text>[^\s](?:.+?(\r\n|\r|\n)?)*?(?<!\\|\s))%)"

    # text
    STRIKETHROUGH_1 = r"(?<!\\)(~(?P<strikethrough1_text>[^\s](?:.+?(\r\n|\r|\n)?)*?(?<!\\|\s))~)"

    # text
    ANCHOR_1 = r"(?<!\\)(?P<anchor1_text><[^\s][\S]*?(?<!\\|\s)>)$(\r\n|\r|\n)?"

    # text
    ITEM_1 = r"(?P<item1_text>(\r\n|\r|\n)?(  )*[-*] )"

    #
    GAP_1 = r"\s*(\r\n|\r|\n)\s*(\r\n|\r|\n)"

    # text
    STRING_1 = r"(?P<string1_text>[\s\S]?)"
