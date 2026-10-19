import json
import subprocess
import sys
from datetime import UTC, datetime


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Runs `python -m streamstats <args>` and returns the result."""

    return subprocess.run(
        [sys.executable, "-m", "streamstats", "analyze", *map(str, args)],
        capture_output=True, text=True, encoding="utf-8", check=False
    )


def to_utc(*args):
    return datetime(*args, tzinfo=UTC)


def ts(value):
    return datetime.fromisoformat(value)


def test_ok_csv(data_dir):
    result = run_cli(data_dir / "events_ok.csv", "--format", "csv")
    assert result.returncode == 0
    json_report = json.loads(result.stdout)
    assert json_report["total"] == 8
    assert json_report["skipped"] == 0
    assert json_report["levels"]["ERROR"] == 3
    assert json_report["sources"]["web"] == 3
    assert json_report["top_error_sources"].get("db") == 2
    assert ts(json_report["first_timestamp"]) == to_utc(2026, 10, 7, 9, 0)
    assert ts(json_report["last_timestamp"]) == to_utc(2026, 10, 7, 9, 6)


def test_jsonl_with_timezone_offsets(data_dir):
    result = run_cli(data_dir / "events_ok.jsonl", "--format", "jsonl")
    assert result.returncode == 0
    json_report = json.loads(result.stdout)
    assert json_report["total"] == 6
    assert ts(json_report["first_timestamp"]) == to_utc(2026, 10, 7, 8, 55)
    assert ts(json_report["last_timestamp"]) == to_utc(2026, 10, 7, 9, 14)


def test_output_file(tmp_path, data_dir):
    out = tmp_path / "report.json"
    result = run_cli(data_dir / "events_ok.csv", "--format", "csv", "--output", out)
    assert result.returncode == 0
    assert json.loads(out.read_text(encoding="utf-8"))["total"] == 8


def test_multiple_files(tmp_path, data_dir):
    second = tmp_path / "second.csv"
    second.write_text(
        "timestamp,level,source,message\n"
        "2026-10-07T08:55:00+00:00,ERROR,auth,Late\n"
        "2026-10-07T09:30:00+00:00,ERROR,db,Extra\n",
        encoding="utf-8",
    )
    result = run_cli(data_dir / "events_ok.csv", second, "--format", "csv")
    assert result.returncode == 0
    json_report = json.loads(result.stdout)
    assert json_report["total"] == 10
    assert json_report["top_error_sources"].get("auth") == 2
    assert ts(json_report["first_timestamp"]) == to_utc(2026, 10, 7, 8, 55)
    assert ts(json_report["last_timestamp"]) == to_utc(2026, 10, 7, 9, 30)


def test_empty_file(data_dir):
    result = run_cli(data_dir / "events_empty.csv", "--format", "csv")
    assert result.returncode == 0
    json_report = json.loads(result.stdout)
    assert json_report["total"] == 0
    assert json_report["first_timestamp"] == "None"
    assert json_report["last_timestamp"] == "None"


def test_unicode(data_dir):
    result = run_cli(data_dir / "events_unicode.csv", "--format", "csv")
    assert result.returncode == 0
    assert "база данных" in result.stdout
    assert json.loads(result.stdout)["sources"]["база данных"] == 2


def test_bad_data_stops_with_code_2(data_dir):
    result = run_cli(data_dir / "events_bad.csv", "--format", "csv")
    assert result.returncode == 2
    assert "events_bad.csv:3" in result.stderr
    assert result.stdout == ""


def test_skip_invalid(data_dir):
    result = run_cli(data_dir / "events_bad.csv", "--format", "csv", "--skip-invalid")
    assert result.returncode == 0
    json_report = json.loads(result.stdout)
    assert json_report["total"] == 3
    assert json_report["skipped"] == 4
    assert result.stderr.count("WARNING") == 4


def test_missing_input_file(tmp_path):
    result = run_cli(tmp_path / "nope.csv", "--format", "csv")
    assert result.returncode == 2
    assert "nope.csv" in result.stderr
