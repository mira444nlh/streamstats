import sys

from streamstats.analysis import analyze_events
from streamstats.cli import check_arguments, parse_arguments
from streamstats.errors import StreamStatsError
from streamstats.report import print_report


def main() -> int:
    try:
        args = parse_arguments()
        check_arguments(args)
        analyzed_data = analyze_events(args.input, args.format, args.skip_invalid)
        print_report(analyzed_data, args.output)
    except StreamStatsError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
