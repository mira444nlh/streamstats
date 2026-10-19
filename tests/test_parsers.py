
from streamstats.errors import InvalidEventError
from streamstats.parsers import parse_csv, parse_jsonl


# CSV
def test_csv_ok(data_dir):
    items = list(parse_csv(data_dir / "events_ok.csv"))
    assert len(items) == 8
    line_num, record = items[0]
    assert line_num == 2
    assert record["level"] == "INFO"


def test_csv_field_ommited_is_empty(data_dir):
    items = list(parse_csv(data_dir / "events_bad.csv"))
    line_num, record = items[1]
    assert line_num == 3
    assert record["source"] == ''


def test_csv_short_row(data_dir):
    items = dict(parse_csv(data_dir / "events_bad.csv"))
    assert items[7]["message"] is None


def test_csv_header_only_is_empty(data_dir):
    assert list(parse_csv(data_dir / "events_empty.csv")) == []


def test_csv_unicode_and_multiline_record(data_dir):
    items = list(parse_csv(data_dir / "events_unicode.csv"))
    assert [n for n, _ in items] == [2, 3, 5, 6]
    assert items[0][1]["source"] == "загрузчик"
    assert items[1][1]["message"] == "Ошибка, соединение потеряно"
    assert "\n" in items[2][1]["message"]
    assert "🐢" in items[3][1]["message"]


# JSONL
def test_jsonl_ok(data_dir):
    items = list(parse_jsonl(data_dir / "events_ok.jsonl"))
    assert len(items) == 6
    line_num, record = items[4]
    assert line_num == 5
    assert "Out of memory" in record["message"]


def test_jsonl_broken_line(data_dir):
    items = list(parse_jsonl(data_dir / "events_bad.jsonl"))
    line_num, record = items[1]
    assert line_num == 2
    assert isinstance(record, InvalidEventError)


def test_jsonl_is_empty(data_dir):
    assert list(parse_jsonl(data_dir / "events_empty.jsonl")) == []


def test_jsonl_line_number_is_from_file_not_from_event_count(data_dir):
    items = list(parse_jsonl(data_dir / "events_bad.jsonl"))
    good_so_far = 0
    for line_num, record in items:
        if isinstance(record, dict):
            good_so_far += 1
    assert good_so_far == 5
    assert items[-1][0] == 7
