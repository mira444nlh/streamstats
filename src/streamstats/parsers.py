import csv
import json
from pathlib import Path


def parse_csv(path: str):
    with Path(path).open(encoding="utf-8", newline="") as file:
        for line in enumerate(csv.DictReader(file)):
            line_number = line[0];
            record = line[1];

            yield (line_number, {
                "timestamp":    record["timestamp"],
                "level":        record["level"],
                "source":       record["source"],
                "message":      record["message"]
            })

def parse_jsonl(path: str):
    with Path(path).open(encoding="utf-8") as file:
        for line in enumerate(file):
            line_number = line[0]
            record = json.loads(line[1])

            yield (line_number, {
                "timestamp":    record["timestamp"],
                "level":        record["level"],
                "source":       record["source"],
                "message":      record["message"]
            })
