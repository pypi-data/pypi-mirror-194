from typing import Any

import pandas as pd

from cronus_eater import _validator


def blank_to_zero(value: Any) -> Any:
    if _validator.is_blank_value(value):
        return 0

    return value


def blank_to_na(value: Any) -> Any:
    if _validator.is_blank_value(value):
        return pd.NA

    return value
