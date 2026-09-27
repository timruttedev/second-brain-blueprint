"""Loader for a small YAML subset, for config files read by scripts here.

Why this exists instead of PyYAML: the scripts in this directory run in
several places, including scheduled cloud agents, and none of them may
depend on a package being installed. Use it when you add a script that
reads a YAML config.

The subset is deliberately small: block mappings, block sequences, scalars,
comments. Everything else is **rejected with a line number** rather than
guessed at, because a config that silently means something other than what
it looks like is worse than one that refuses to load.

Supported:
    key: value
    key:
      nested: value
    list:
      - scalar
      - key: value        # sequence of mappings, further keys indented below
    "quoted: value"       # single and double quotes
    # comments, blank lines, a leading document marker

Rejected:
    tabs for indentation, anchors and aliases (& *), block scalars (| >),
    flow collections ({} []), multiple documents, duplicate keys.
"""

from __future__ import annotations

import re
from typing import Any

KEY = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_.\-]*)\s*:(?:[ \t]+(.*))?$")


class YamlError(ValueError):
    """Raised with a line number whenever the input leaves the subset."""


class _Line:
    __slots__ = ("no", "indent", "text")

    def __init__(self, no: int, indent: int, text: str) -> None:
        self.no = no
        self.indent = indent
        self.text = text

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"_Line({self.no}, {self.indent}, {self.text!r})"


def _strip_comment(text: str) -> str:
    """Drop a trailing comment, respecting quotes."""
    quote = ""
    for i, ch in enumerate(text):
        if quote:
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or text[i - 1] in " \t"):
            return text[:i].rstrip()
    return text.rstrip()


def _scalar(raw: str, no: int) -> Any:
    text = raw.strip()
    if text.startswith(("&", "*")):
        raise YamlError(f"line {no}: anchors and aliases are not supported")
    if text in ("|", ">") or text.startswith(("|", ">")) and len(text) <= 2:
        raise YamlError(f"line {no}: block scalars are not supported")
    if text.startswith(("{", "[")):
        raise YamlError(f"line {no}: flow collections are not supported, use block style")
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    text = _strip_comment(text)
    if text in ("", "~", "null"):
        return None
    if text == "true":
        return True
    if text == "false":
        return False
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    return text


def _lines(src: str) -> list[_Line]:
    out: list[_Line] = []
    for no, raw in enumerate(src.splitlines(), start=1):
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise YamlError(f"line {no}: tabs must not be used for indentation")
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "---":
            if out:
                raise YamlError(f"line {no}: only a single document is supported")
            continue
        if stripped == "...":
            break
        out.append(_Line(no, len(raw) - len(raw.lstrip(" ")), _strip_comment(raw.strip())))
    return out


class _Parser:
    def __init__(self, lines: list[_Line]) -> None:
        self.lines = lines
        self.pos = 0

    def at_end(self) -> bool:
        return self.pos >= len(self.lines)

    def peek(self) -> _Line:
        return self.lines[self.pos]

    def block(self, indent: int) -> Any:
        if self.at_end():
            return None
        if self.peek().text.startswith("- ") or self.peek().text == "-":
            return self.sequence(indent)
        return self.mapping(indent)

    def mapping(self, indent: int) -> dict[str, Any]:
        result: dict[str, Any] = {}
        while not self.at_end():
            line = self.peek()
            if line.indent < indent:
                break
            if line.indent > indent:
                raise YamlError(f"line {line.no}: unexpected indentation inside a mapping")
            if line.text.startswith("- "):
                break
            match = KEY.match(line.text)
            if not match:
                raise YamlError(f"line {line.no}: expected 'key: value', got {line.text!r}")
            key, inline = match.group(1), match.group(2)
            if key in result:
                raise YamlError(f"line {line.no}: duplicate key {key!r}")
            self.pos += 1
            if inline is not None and inline.strip() != "":
                result[key] = _scalar(inline, line.no)
                continue
            if self.at_end() or self.peek().indent <= indent:
                result[key] = None
                continue
            result[key] = self.block(self.peek().indent)
        return result

    def sequence(self, indent: int) -> list[Any]:
        result: list[Any] = []
        while not self.at_end():
            line = self.peek()
            if line.indent < indent:
                break
            if line.indent > indent:
                raise YamlError(f"line {line.no}: unexpected indentation inside a sequence")
            if not (line.text.startswith("- ") or line.text == "-"):
                break
            rest = line.text[2:].strip() if line.text.startswith("- ") else ""
            self.pos += 1
            item_indent = line.indent + 2
            match = KEY.match(rest) if rest else None
            if match:
                # A mapping starts on the dash line. Re-inject it at the item
                # indentation so the ordinary mapping parser can take over.
                self.lines.insert(self.pos, _Line(line.no, item_indent, rest))
                result.append(self.mapping(item_indent))
            elif rest:
                result.append(_scalar(rest, line.no))
            else:
                if self.at_end() or self.peek().indent <= line.indent:
                    result.append(None)
                else:
                    result.append(self.block(self.peek().indent))
        return result


def loads(src: str) -> Any:
    """Parse the YAML subset. Raises YamlError with a line number on anything else."""
    parser = _Parser(_lines(src))
    if parser.at_end():
        return None
    value = parser.block(parser.peek().indent)
    if not parser.at_end():
        raise YamlError(f"line {parser.peek().no}: trailing content that is not part of the document")
    return value


def load(path: str) -> Any:
    with open(path, encoding="utf-8") as handle:
        return loads(handle.read())
