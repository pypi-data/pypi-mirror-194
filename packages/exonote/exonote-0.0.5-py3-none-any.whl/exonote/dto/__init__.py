from collections import namedtuple


Token = namedtuple("Token", ["element", "data"])

HeadingInfo = namedtuple("HeadingInfo", ["sid", "index", "index_end", "level", "text"])

SectionInfo = namedtuple("SectionInfo", ["sid", "index", "index_end", "heading", "level", "text"])

ProgramContext = namedtuple("ProgramContext", ["viewer", "arguments"])

PageInfo = namedtuple("IndexEntry", ["filename", "page", "title", "tags"])
