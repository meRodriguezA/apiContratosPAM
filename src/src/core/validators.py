import re
from datetime import datetime


def is_date_dd_mm_yyyy(value: str) -> bool:
    value = str(value).strip()

    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", value):
        return False

    try:
        datetime.strptime(value, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def min_length(value: str, length: int) -> bool:
    return len(str(value).strip()) >= length
