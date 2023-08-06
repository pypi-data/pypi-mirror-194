# Cronus Eater: A simple tool to get time series from spreadsheets

<div align="center">
  <img width="450" height="278" src="https://raw.githubusercontent.com/breno-jesus-fernandes/cronus-eater/main/docs/img/cronus-eater-logo.png"><br>
</div>

[![Test](https://github.com/breno-jesus-fernandes/cronus-eater/actions/workflows/test.yaml/badge.svg)](https://github.com/breno-jesus-fernandes/cronus-eater/actions/workflows/test.yaml)
[![PyPI Latest Release](https://img.shields.io/pypi/v/cronus-eater.svg)](https://pypi.org/project/cronus-eater/)
[![Package Status](https://img.shields.io/pypi/status/cronus-eater.svg)](https://pypi.org/project/cronus-eater/)
[![Python: 3.7 | 3.8 | 3.9 | 3.10 | 3.11](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://pypi.org/project/cronus-eater/)
[![Downloads](https://static.pepy.tech/badge/cronus-eater)](https://pepy.tech/project/cronus-eater)
[![Code style: blue](https://img.shields.io/badge/code%20style-blue-blue.svg)](https://github.com/grantjenks/blue)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) 
[![LICENSE](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/breno-jesus-fernandes/cronus-eater/blob/main/LICENSE)

Extract and normalize time series from any spreadsheet with differents patterns.


### Where is the data I want?

```python

import pandas as pd

raw_dataframe = pd.read_excel('historical_series_3Q22.xlsx')
raw_dataframe.head()

```

|     |  0  |              1              |  2  |  3  |    4     |     5    |    6    |    7     |    8      |  9  |
| --- | --- | --------------------------- | --- | --- | -------  | -------  | ------  | -------  | -------   | ----|
| 0   | NaN | NaN                         | NaN | NaN |   NaN    |   NaN    |   NaN   |    NaN   |    NaN    | NaN |
| 1   | NaN | Holdings Ltd.               | NaN | NaN |   NaN    |   NaN    |   NaN   |    NaN   |    NaN    | NaN |
| 2   | NaN | NaN                         | NaN | NaN |   3Q22   |   2Q22   |   NaN   |   1Q22   |   2022    | NaN |
| 3   | NaN | Amounts in thousands of R$  | NaN | NaN |   R$     |   R$     |   NaN   |    R$    |    R$     | NaN |
| 4   | NaN | Cash Flow                   | NaN | NaN | $500.23  | $302.81  |   NaN   | $106.12  |  $900.00  | NaN |

### Let's devours this times series  

```python

import cronus_eater
times_series_df = cronus_eater.extract(raw_dataframe)
times_series_df.head()

```


|     | Numeric Index | Label Index | Table Order | Time | Value   |
| --- | ------------- | ---------   | ----------- | ---- | ------- |
| 0   |  4            | Cash Flow   | 1           | 3Q22 | 500.23  |
| 1   |  4            | Cash Flow   | 1           | 2Q22 | 302.81  |
| 2   |  4            | Cash Flow   | 1           | 1Q22 | 106.12  |
| 3   |  4            | Cash Flow   | 1           | 2022 | 900.00  |


## Where to get it

The source code is currently hosted on GitHub at: <https://github.com/breno-jesus-fernandes/cronus-eater>

Binary installers for the latest released version is going to available at the [Python Package Index (PyPI)](https://pypi.org/project/cronus-eater).


```sh
pip install cronus-eater
# or through poetry
poetry add cronus-eater
```

## License

[MIT](https://github.com/breno-jesus-fernandes/cronus-eater/blob/main/LICENSE)

## Contributing to Cronus Eater
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. See https://github.com/breno-jesus-fernandes/cronus-eater/tree/main/docs for instructions.



 