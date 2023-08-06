# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cronus_eater']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'openpyxl>=3.0.10,<4.0.0', 'unidecode>=1.3.6,<2.0.0']

extras_require = \
{':python_full_version >= "3.7.1" and python_version < "3.8"': ['pandas==1.3.5'],
 ':python_version >= "3.8" and python_version < "3.12"': ['pandas>=1.5.0,<2.0.0']}

entry_points = \
{'console_scripts': ['cronus-eater = cronus_eater.__main__:main']}

setup_kwargs = {
    'name': 'cronus-eater',
    'version': '0.1.0a7',
    'description': 'A simple tool to get time series from spreadsheets',
    'long_description': '# Cronus Eater: A simple tool to get time series from spreadsheets\n\n<div align="center">\n  <img width="450" height="278" src="https://raw.githubusercontent.com/breno-jesus-fernandes/cronus-eater/main/docs/img/cronus-eater-logo.png"><br>\n</div>\n\n[![Test](https://github.com/breno-jesus-fernandes/cronus-eater/actions/workflows/test.yaml/badge.svg)](https://github.com/breno-jesus-fernandes/cronus-eater/actions/workflows/test.yaml)\n[![PyPI Latest Release](https://img.shields.io/pypi/v/cronus-eater.svg)](https://pypi.org/project/cronus-eater/)\n[![Package Status](https://img.shields.io/pypi/status/cronus-eater.svg)](https://pypi.org/project/cronus-eater/)\n[![Python: 3.7 | 3.8 | 3.9 | 3.10 | 3.11](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://pypi.org/project/cronus-eater/)\n[![Downloads](https://static.pepy.tech/badge/cronus-eater)](https://pepy.tech/project/cronus-eater)\n[![Code style: blue](https://img.shields.io/badge/code%20style-blue-blue.svg)](https://github.com/grantjenks/blue)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) \n[![LICENSE](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/breno-jesus-fernandes/cronus-eater/blob/main/LICENSE)\n\nExtract and normalize time series from any spreadsheet with differents patterns.\n\n\n### Where is the data I want?\n\n```python\n\nimport pandas as pd\n\nraw_dataframe = pd.read_excel(\'historical_series_3Q22.xlsx\')\nraw_dataframe.head()\n\n```\n\n|     |  0  |              1              |  2  |  3  |    4     |     5    |    6    |    7     |    8      |  9  |\n| --- | --- | --------------------------- | --- | --- | -------  | -------  | ------  | -------  | -------   | ----|\n| 0   | NaN | NaN                         | NaN | NaN |   NaN    |   NaN    |   NaN   |    NaN   |    NaN    | NaN |\n| 1   | NaN | Holdings Ltd.               | NaN | NaN |   NaN    |   NaN    |   NaN   |    NaN   |    NaN    | NaN |\n| 2   | NaN | NaN                         | NaN | NaN |   3Q22   |   2Q22   |   NaN   |   1Q22   |   2022    | NaN |\n| 3   | NaN | Amounts in thousands of R$  | NaN | NaN |   R$     |   R$     |   NaN   |    R$    |    R$     | NaN |\n| 4   | NaN | Cash Flow                   | NaN | NaN | $500.23  | $302.81  |   NaN   | $106.12  |  $900.00  | NaN |\n\n### Let\'s devours this times series  \n\n```python\n\nimport cronus_eater\ntimes_series_df = cronus_eater.extract(raw_dataframe)\ntimes_series_df.head()\n\n```\n\n\n|     | Numeric Index | Label Index | Table Order | Time | Value   |\n| --- | ------------- | ---------   | ----------- | ---- | ------- |\n| 0   |  4            | Cash Flow   | 1           | 3Q22 | 500.23  |\n| 1   |  4            | Cash Flow   | 1           | 2Q22 | 302.81  |\n| 2   |  4            | Cash Flow   | 1           | 1Q22 | 106.12  |\n| 3   |  4            | Cash Flow   | 1           | 2022 | 900.00  |\n\n\n## Where to get it\n\nThe source code is currently hosted on GitHub at: <https://github.com/breno-jesus-fernandes/cronus-eater>\n\nBinary installers for the latest released version is going to available at the [Python Package Index (PyPI)](https://pypi.org/project/cronus-eater).\n\n\n```sh\npip install cronus-eater\n# or through poetry\npoetry add cronus-eater\n```\n\n## License\n\n[MIT](https://github.com/breno-jesus-fernandes/cronus-eater/blob/main/LICENSE)\n\n## Contributing to Cronus Eater\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. See https://github.com/breno-jesus-fernandes/cronus-eater/tree/main/docs for instructions.\n\n\n\n ',
    'author': 'Breno Fernandes',
    'author_email': 'breno.de.jesus.fernandes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/breno-jesus-fernandes/cronus-eater',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.12',
}


setup(**setup_kwargs)
