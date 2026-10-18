import argparse
import sys

from streamstats.analysis import analyze_events
from streamstats.errors import StreamStatsError
from streamstats.report import print_report


def analyze(args):
    try:
        data = analyze_events(args.input, args.format, args.skip_invalid)
        print_report(data, args.output)
    except StreamStatsError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)

def main() -> None:
    parser = argparse.ArgumentParser(description="Потоковый анализатор файлов")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступные команды")
    analyze_parser = subparsers.add_parser("analyze", help="Анализировать файлы")

    analyze_parser.add_argument(
        "input",
        nargs="+",
        metavar="INPUT",
        help="Пути к входным файлам"
    )

    analyze_parser.add_argument(
        "--format",
        choices=["csv", "jsonl"],
        required=True,
        help="Формат входных данных"
    )

    analyze_parser.add_argument(
        "--output",
        default=None,
        metavar="REPORT.json",
        help="Пути для сохранения итогового отчета в формате JSON"
    )

    analyze_parser.add_argument(
        "--skip-invalid",
        action="store_true",
        help="Пропуск неверной строки"
    )

    analyze_parser.set_defaults(func=analyze)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
