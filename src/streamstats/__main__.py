from streamstats.analysis import analyse_events
from streamstats.report import print_report


def main() -> None:
    data = analyse_events([".data/events_ok.csv"], "csv")
    print_report(data)


if __name__ == "__main__":
    main()
