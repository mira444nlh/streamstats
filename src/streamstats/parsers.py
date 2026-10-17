import csv
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def parse_csv(path: str) -> Iterator[tuple[int, dict[str, str]]]:
    with Path(path).open(encoding="utf-8", newline="") as file:
        for line in enumerate(csv.DictReader(file)):
            line_number = line[0]
            record = line[1]

            yield (line_number, {
                "timestamp":    record["timestamp"].strip(),
                "level":        record["level"].strip(),
                "source":       record["source"].strip(),
                "message":      record["message"].strip()
            })

def parse_jsonl(path: str) -> Iterator[tuple[int, dict[str, Any]]]:
    with Path(path).open(encoding="utf-8") as file:
        for line in enumerate(file):
            line_number = line[0]
            record = json.loads(line[1])

            yield (line_number, {
                "timestamp":    record["timestamp"].strip(),
                "level":        record["level"].strip(),
                "source":       record["source"].strip(),
                "message":      record["message"].strip()
            })
