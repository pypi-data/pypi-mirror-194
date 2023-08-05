from datetime import datetime
from typing import Any, List

import numpy as np
import pandas as pd

from cronus_eater import _validator
from cronus_eater.model import TimeSeries


def norm_blank_value(value: Any) -> Any:
    if _validator.is_blank_value(value):
        return pd.NA

    return value


def norm_header(value: Any) -> Any:
    if isinstance(value, datetime):
        value = f'{pd.Timestamp(value).quarter}T{str(value.year)[2:]}'
        return value

    return value
