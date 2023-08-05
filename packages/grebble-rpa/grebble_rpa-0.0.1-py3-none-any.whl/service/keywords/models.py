import re
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
class Param:
    name: str

    def __init__(self, name=None):
        if name:
            self.name = name


@dataclass_json
class Keyword:
    name: str
    short_doc: str
    doc: str
    params: List[Param]

    def __init__(self, name=None, short_doc=None, doc=None, params: List[Param] = []):
        self.short_doc = short_doc
        self.doc = doc
        if name:
            self.name = re.sub(
                r"\b[a-z]", lambda m: m.group().upper(), name.replace("_", " ")
            )

        self.params = params
