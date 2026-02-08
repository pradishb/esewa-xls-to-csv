from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

import xlrd  # type: ignore

from esewa_xls_to_csv.utils import convert_date


@dataclass
class Statement:
    date: str
    description: str
    debit: Decimal
    credit: Decimal
    balance: Decimal


def parse_statement_from_xls(file_path: Path):
    rows: list[Statement] = []
    book: Any = xlrd.open_workbook(file_path)  # type: ignore
    sh = book.sheet_by_index(0)
    # eSewa statement starts from row 10
    for rx in range(9, sh.nrows):
        ref = sh.cell_value(rowx=rx, colx=0)
        date = sh.cell_value(rowx=rx, colx=1)
        detail = sh.cell_value(rowx=rx, colx=2)
        debit = sh.cell_value(rowx=rx, colx=3)
        credit = sh.cell_value(rowx=rx, colx=4)
        balance = sh.cell_value(rowx=rx, colx=6)
        date = convert_date(date)
        if date and ref and detail:
            row = Statement(
                date=date,
                description=ref + ", " + detail,
                debit=Decimal(debit),
                credit=Decimal(credit),
                balance=Decimal(balance),
            )
            rows.append(row)
    return rows
