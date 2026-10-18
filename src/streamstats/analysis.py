from datetime import datetime

from streamstats.models import Event, Level, iter_events


class Accumulator:
    def __init__(self) -> None:
        self.total_acc: int = 0
        self.skipped_acc: int = 0
        self.level_acc: dict[Level, int] = {
            Level.DEBUG: 0,
            Level.INFO: 0,
            Level.WARNING: 0,
            Level.ERROR: 0,
            Level.CRITICAL: 0
        }
        self.source_acc: dict[str, int] = {}
        self.error_sources: dict[str, int] = {}
        self.first_timestamp: datetime | None = None
        self.last_timestamp: datetime | None = None

    def add(self, event: Event) -> None:
        self.total_acc += 1
        self.level_acc[event.level] += 1

        if event.source in self.source_acc:
            self.source_acc[event.source] += 1
        else:
            self.source_acc[event.source] = 1

        if event.level in (Level.ERROR, Level.CRITICAL):
            if event.source in self.error_sources:
                self.error_sources[event.source] += 1
            else:
                self.error_sources[event.source] = 1

        if self.first_timestamp is None or event.timestamp < self.first_timestamp:
            self.first_timestamp = event.timestamp

        if self.last_timestamp is None or event.timestamp > self.last_timestamp:
            self.last_timestamp = event.timestamp

    def add_skip(self) -> None:
        self.skipped_acc += 1

    def get_top5_sources(self) -> list[tuple[str, int]]:
        return sorted(self.error_sources.items(), key=lambda el: (-el[1], el[0]))[:5]


def analyze_events(paths: list[str], fmt: str, skip_invalid: bool) -> Accumulator:
    acc = Accumulator()
    for path in paths:
        for event in iter_events(path, fmt, skip_invalid, acc.add_skip):
            acc.add(event)

    return acc
