import csv
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from streamstats.errors import InvalidEventError, UnsupportedFormatError


def parse_csv(path: str) -> Iterator[tuple[int, dict[str, Any]]]:
    with Path(path).open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for record in reader:
            yield reader.line_num, record


def parse_jsonl(path: str) -> Iterator[tuple[int, dict[str, Any] | InvalidEventError]]:
    with Path(path).open(encoding="utf-8") as file:
        for line_number, text in enumerate(file, start=1):
            if not text.strip():
                continue

            try:
                record = json.loads(text)
            except json.JSONDecodeError as err:
                yield line_number, InvalidEventError(f"Некорректный JSON: {err.msg}")
                continue
            if not isinstance(record, dict):
                yield line_number, InvalidEventError("Строка JSONL не является объектом")
                continue
            yield line_number, record


def get_parser(fmt: str):
    parsers = {"csv": parse_csv, "jsonl": parse_jsonl}
    try:
        return parsers[fmt]
    except KeyError:
        raise UnsupportedFormatError(f"Неподдерживаемый формат: {fmt!r}") from None
