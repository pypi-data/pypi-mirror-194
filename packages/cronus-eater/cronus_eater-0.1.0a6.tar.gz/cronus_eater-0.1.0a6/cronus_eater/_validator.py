import re
from datetime import datetime
from typing import Any, List, Union

import numpy as np
import pandas as pd


def is_blank_value(value: Any) -> bool:

    if pd.isnull(value):
        return True

    if len(str(value).strip()) == 0:
        return True

    if str(value).strip().lower() in ('-', 'none', 'null', 'nan'):
        return True

    return False


def is_normal_number(value: str) -> bool:
    if re.match(r'[$]?[\s]?[-]?[\d]+(([.]|[,])[\d]+)?$', value):
        return True

    return False


def is_number_with_comma_sep(value: str) -> bool:
    if re.match(r'[$]?[\s]?[-]?[\d]{1,3}([,][\d]{3})*([.][\d]+)?$', value):
        return True

    return False


def is_number_with_dot_sep(value: str) -> bool:
    if re.match(r'[$]?[\s]?[-]?[\d]{1,3}([.][\d]{3})*([,][\d]+)?$', value):
        return True

    return False


def is_number_with_space_sep(value: str) -> bool:
    if re.match(
        r'[$]?[\s]?[-]?[\d]{1,3}([\s][\d]{3})*(([.]|[,])[\d]+)?$', value
    ):
        return True

    return False


def is_percent_number(value: str) -> bool:
    if re.match(r'[-]?[\d]+(([.]|[,])[\d]+)?[\s]?[%]$', value):
        return True

    return False


def is_number_type(value: Union[float, int, np.number]) -> bool:
    return isinstance(value, (float, int, np.number))


def is_year(value: Any) -> bool:

    if is_blank_value(value):
        return False

    text_value = str(value).strip()
    if re.match(
        r'(([1][9])|([2][0-1]))[0-9][0-9](([.]|[,]|[\s])([0-4]|([0][1-9])|([1][0-2])))?$',
        text_value,
    ):
        return True
    return False


def is_financial_number(value: Any) -> bool:

    if is_blank_value(value):
        return False

    text = str(value).strip()

    if (
        is_normal_number(text)
        or is_number_with_dot_sep(text)
        or is_number_with_comma_sep(text)
        or is_number_with_space_sep(text)
        or is_percent_number(text)
    ):
        return True

    return False


def is_text(value: Any) -> bool:
    return (
        not is_date_time(value)
        and not is_blank_value(value)
        and not is_financial_number(value)
    )


def is_time_series_row(row: pd.Series) -> bool:
    sequence_text: List[str] = []
    sequence_numbers: List[str] = []

    # If is a empty sequence return false
    if len(row.dropna()) == 0:
        return False

    # Calcule the right pattern of a time series row
    for value in row:
        if (is_text(value) or is_date_time(value)) and len(
            sequence_numbers
        ) == 0:
            sequence_text.append(str(value))
        elif is_financial_number(value) and len(sequence_text) in (1, 2, 3):
            sequence_numbers.append(str(value))
        elif (is_text(value) or is_date_time(value)) and len(
            sequence_numbers
        ) > 0:
            break

    # if a sequence is empty means we do not have a time series pattern
    if 0 in (len(sequence_numbers), len(sequence_text)):
        return False

    return True


def is_text_row(row: pd.Series) -> bool:
    # If is a empty sequence return false
    if len(row.dropna()) == 0:
        return False

    # If there is at least one number is not a text row
    n_text = 0
    for value in row:
        if is_text(value) or is_date_time(value):
            n_text += 1

    if n_text >= 3:
        return True

    return False


def is_date_time(value: Any) -> bool:

    if is_blank_value(value):
        return False

    if isinstance(value, datetime) or is_year(value):
        return True

    text = str(value).strip()
    if re.match(
        r'(\b(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4}|\d{2})\b)|(\b(0?[1-9]|1[0-2])[^\w\d\r\n:](0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](\d{4}|\d{2})\b)',
        text,
    ):
        return True
    elif re.match(r'[1-4]([Q]|[T])[\s]?[1-2]?[0-9]?[0-9][0-9]', text):
        return True
    elif re.match(r'[1-12][M][\s]?[1-2]?[0-9]?[0-9][0-9]', text):
        return True

    return False
