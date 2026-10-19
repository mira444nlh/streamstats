import pytest

from streamstats.errors import (
    InvalidEventError,
    InvalidTimestampError,
    UnsupportedFormatError,
)
from streamstats.models import Event, Level, iter_events, validate_record


def make_record(**changes: str) -> dict[str, str]:
    """Creates a log record dict, overriding the default fields with the provided arguments."""

    record = {
        "timestamp": "2026-10-07T09:00:00+00:00",
        "level": "INFO",
        "source": "web",
        "message": "hello",
    }
    record.update(changes)
    return record


# validation tests
def test_valid_record():
    event = validate_record(make_record())
    assert isinstance(event, Event)
    assert event.level == Level.INFO
    assert event.source == "web"
    assert event.message == "hello"


def test_missing_field():
    record = make_record()
    del record["source"]
    with pytest.raises(InvalidEventError):
        validate_record(record)


def test_unknown_level():
    with pytest.raises(InvalidEventError):
        validate_record(make_record(level="1234"))


def test_empty_source():
    with pytest.raises(InvalidEventError):
        validate_record(make_record(source="   "))


def test_bad_timestamp():
    with pytest.raises(InvalidTimestampError):
        validate_record(make_record(timestamp="invalid-date"))


# iter events tests
def test_iter_events_ok(data_dir):
    events = list(iter_events(data_dir / "events_ok.csv", "csv"))
    assert len(events) == 8


def test_stops_on_bad_csv_line(data_dir):
    with pytest.raises(InvalidEventError, match="events_bad.csv:3"):
        list(iter_events(data_dir / "events_bad.csv", "csv"))


def test_stops_on_bad_jsonl_line(data_dir):
    with pytest.raises(InvalidEventError, match="events_bad.jsonl:2"):
        list(iter_events(data_dir / "events_bad.jsonl", "jsonl"))


def test_unsupported_format(data_dir):
    with pytest.raises(UnsupportedFormatError):
        list(iter_events(data_dir / "events_ok.csv", "unk"))
