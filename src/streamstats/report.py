import json
from pathlib import Path

from streamstats.analysis import Accumulator


def print_report(acc: Accumulator, output: str | None = None) -> None:
    """Serialize the statistics as JSON and write them out."""

    acc_dict = {
        "total": acc.total_acc,
        "skipped": acc.skipped_acc,
        "levels": {key.name: value for key, value in acc.level_acc.items()},
        "sources": acc.source_acc,
        "top_error_sources": acc.get_top5_sources(),
        "first_timestamp": str(acc.first_timestamp),
        "last_timestamp": str(acc.last_timestamp)
    }
    report_text = json.dumps(acc_dict, indent=2, ensure_ascii=False)
    if output:
        with Path(output).open(mode='w', encoding="utf-8") as out:
            print(report_text, file=out)
    else:
        print(report_text)
