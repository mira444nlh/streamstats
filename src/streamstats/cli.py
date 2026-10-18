import argparse
from pathlib import Path

from streamstats.errors import CLIConfigError


class StreamStatsParser(argparse.ArgumentParser):
    def error(self, message):
        raise CLIConfigError(message)


def parse_arguments() -> argparse.Namespace:
    parser = StreamStatsParser(description="Потоковый анализатор файлов")

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

    return parser.parse_args()


def check_arguments(args: argparse.Namespace) -> None:
    for input in args.input:
        if not Path(input).is_file():
            raise CLIConfigError(f"Входной файл не найден: {input}")
    if args.output and Path(args.output) in map(Path, args.input):
        raise CLIConfigError("--output совпадает с входным файлом")
