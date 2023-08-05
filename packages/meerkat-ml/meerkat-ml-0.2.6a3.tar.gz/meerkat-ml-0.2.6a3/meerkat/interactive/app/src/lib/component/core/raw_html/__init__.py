from typing import Any, Dict

from meerkat.interactive.app.src.lib.component.abstract import Component


class RawHTML(Component):
    html: str
    view: str = "full"