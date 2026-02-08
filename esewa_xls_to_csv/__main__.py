import csv
from argparse import ArgumentParser
from pathlib import Path

from esewa_xls_to_csv.xls import parse_statement_from_xls


def get_is_substr(sub: str, text: str):
    return sub.replace(" ", "").upper() in text.replace(" ", "").upper()


def main():
    parser = ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--delimiter", default=";")
    parser.add_argument("--output", default="output.csv")
    args = parser.parse_args()
    file_path = Path(args.input)

    if file_path.suffix not in [".xls", ".pdf"]:
        print("Invalid input format")
        return

    statement = parse_statement_from_xls(file_path)
    with open(args.output, "w", newline="") as fp:
        writer = csv.writer(fp, delimiter=args.delimiter)
        for s in statement:
            if s.debit > 0 and s.credit > 0:
                print("bad row, debit and credit both greater than 0", s)
                continue
            elif s.credit > 0:
                writer.writerow(
                    [
                        s.date,
                        4,
                        "",
                        "",
                        s.description,
                        s.credit,
                        "",
                        "",
                    ]
                )
            elif s.debit > 0:
                writer.writerow(
                    [
                        s.date,
                        4,
                        "",
                        "",
                        s.description,
                        s.debit * -1,
                        "",
                        "",
                    ]
                )


if __name__ == "__main__":
    main()
