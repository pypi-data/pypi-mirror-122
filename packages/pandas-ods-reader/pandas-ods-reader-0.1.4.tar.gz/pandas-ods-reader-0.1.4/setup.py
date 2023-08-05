# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_ods_reader', 'pandas_ods_reader.parsers']

package_data = \
{'': ['*']}

install_requires = \
['ezodf>=0.3.2,<0.4.0', 'lxml>=4.6.3,<5.0.0', 'pandas>=1.0.0,<2.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib_metadata>=4.8.1,<5.0.0']}

setup_kwargs = {
    'name': 'pandas-ods-reader',
    'version': '0.1.4',
    'description': 'Read in .ods and .fods files and return a pandas.DataFrame.',
    'long_description': 'pandas-ods-reader\n===\n\nProvides a function to read in a **.ods** or **.fods** file and returns a pandas DataFrame.\n\nIt uses `ezodf` to read in **.ods** files. Since **.fods** files are essentially xml, `lxml` is used to read them. The correct parser is automatically chosen based on the file\'s extension.\n\nIf a range is specified in the sheet to be imported, it seems that `ezodf` imports empty cells as well. Therefore, completely empty rows and columns are dropped from the DataFrame, before it is returned. Only trailing empty rows and columns are dropped.\n\nIf the ODS file contains duplicated column names, they will be numbered and the number is appended to the column name in the resulting DataFrame.\n\nDependencies\n---\n\n-   `ezodf`\n-   `lxml`\n-   `pandas`\n\nInstallation\n---\n\n`pip install pandas-ods-reader`\n\nUsage\n---\n\n```Python\nfrom pandas_ods_reader import read_ods\n\npath = "path/to/file.ods"\n\n# by default the first sheet is imported\ndf = read_ods(path)\n\n# load a sheet based on its index (1 based)\nsheet_idx = 2\ndf = read_ods(path, sheet_idx)\n\n# load a sheet based on its name\nsheet_name = "sheet1"\ndf = read_ods(path, sheet_name)\n\n# load a file that does not contain a header row\n# if no columns are provided, they will be numbered\ndf = read_ods(path, 1, headers=False)\n\n# load a file and provide custom column names\n# if headers is True (the default), the header row will be overwritten\ndf = read_ods(path, 1, columns=["A", "B", "C"])\n```\n',
    'author': 'iuvbio',
    'author_email': 'iuvbio@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/iuvbio/pandas_ods_reader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
