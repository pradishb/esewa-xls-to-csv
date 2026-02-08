import re

date_re = r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\.\d"


def convert_date(string: str) -> str:
    match = re.fullmatch(date_re, string)
    if match:
        y, m, d = match.group(1), match.group(2), match.group(3)
        # convert to m-d-y
        return m + "-" + d + "-" + y
    return ""
