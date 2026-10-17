from collections.abc import Callable, Iterator
from datetime import datetime
from enum import Enum, auto
from typing import Any

from streamstats.errors import InvalidEventError, InvalidTimestampError
from streamstats.parsers import parse_csv, parse_jsonl


class Level(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class Event:
    def __init__(self, timestamp: datetime, level: Level, source: str, message: str):
        self.timestamp: datetime = timestamp
        self.level: Level = level
        self.source: str = source
        self.message: str = message


def validate_record(record: dict[str, Any]) -> Event:
    required_fields = ("timestamp", "level", "source", "message")
    missing = [field for field in required_fields if record.get(field) is None]
    if missing:
        raise InvalidEventError(f"Пропущенные поля: {', '.join(missing)}")

    try:
        timestamp = datetime.fromisoformat(record["timestamp"])
    except (ValueError, TypeError):
        raise InvalidTimestampError(f"Неверный формат времени: {record['timestamp']!r}") from None

    try:
        level = Level[record["level"]]
    except KeyError:
        raise InvalidEventError(f"Неизвестный level: {record['level']!r}") from None


    source = record["source"]
    if not isinstance(source, str) or not source.strip():
        raise InvalidEventError(f"Некорректный source: {source!r}")

    message = record["message"]
    if not isinstance(message, str):
        raise InvalidEventError(f"Некорректный message: {message!r}")

    return Event(timestamp, level, source, message)


def iter_events(path: str, fmt: str, skip_invalid: bool = False, on_skip: Callable[[], None] | None = None) -> Iterator[Event]:
    if (fmt == "csv"):
        parser = parse_csv
    else:
        parser = parse_jsonl

    for line_num, record in parser(path):
        try:
            yield validate_record(record)
        except InvalidEventError as e:
            if not skip_invalid:
                raise InvalidEventError(f"{path}:{line_num}: {e}")
            # todo: log this
            if on_skip:
                on_skip()
