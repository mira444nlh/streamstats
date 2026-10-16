from streamstats.models import validate_record
from streamstats.parsers import parse_csv


def main() -> None:
    # pass
    data = parse_csv(".data/events_ok.csv")
    for row in data:
        record = row[1]
        valid_rec = validate_record(record)
        print(valid_rec.message)

if __name__ == "__main__":
    main()
