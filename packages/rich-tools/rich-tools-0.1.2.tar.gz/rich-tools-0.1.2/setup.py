# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.3,<2.0.0', 'rich>=10.12.0,<11.0.0']

setup_kwargs = {
    'name': 'rich-tools',
    'version': '0.1.2',
    'description': 'A python package with helpful tools when working with the rich python library.',
    'long_description': '# 🔧 Rich Tools\n[![Tests](https://github.com/avi-perl/rich_tools/actions/workflows/python-app.yml/badge.svg)](https://github.com/avi-perl/rich_tools/actions/workflows/python-app.yml)\n\nA python package with helpful tools when working with the [rich](https://github.com/willmcgugan/rich) python library.\n\nThe current features are:\n\n- Convert a [Pandas](https://pandas.pydata.org/) DataFrame into a [rich](https://github.com/willmcgugan/rich) Table.\n\n  By making this conversion, we can now pretty print a DataFrame in the terminal with rich. Bridging the gap between \n  pandas and rich also provides a path for loading external data into a rich Table using Pandas functions such as `.from_csv()`!\n- Convert a [rich](https://github.com/willmcgugan/rich) Table into a [Pandas](https://pandas.pydata.org/) DataFrame.\n\n  By bridging the gap between a rich Table and a DataFrame, we can now take additional actions on our data such as   \n  saving the data to a csv using the Pandas function `.to_csv()`!\n\n### Installation\n```bash\n$ pip install rich-tools\n```\n\n### Example\nAdditional examples can be found in the `examples` dir.\n```python\nfrom datetime import datetime\n\nimport pandas as pd\nfrom rich import box\nfrom rich.console import Console\nfrom rich.table import Table\n\nfrom rich_tools.table import df_to_table\n\nconsole = Console()\n\n\nif __name__ == "__main__":\n    sample_data = {\n        "Date": [\n            datetime(year=2019, month=12, day=20),\n            datetime(year=2018, month=5, day=25),\n            datetime(year=2017, month=12, day=15),\n        ],\n        "Title": [\n            "Star Wars: The Rise of Skywalker",\n            "[red]Solo[/red]: A Star Wars Story",\n            "Star Wars Ep. VIII: The Last Jedi",\n        ],\n        "Production Budget": ["$275,000,000", "$275,000,000", "$262,000,000"],\n        "Box Office": ["$375,126,118", "$393,151,347", "$1,332,539,889"],\n    }\n    df = pd.DataFrame(sample_data)\n\n    # Initiate a Table instance to be modified\n    table = Table(show_header=True, header_style="bold magenta")\n\n    # Modify the table instance to have the data from the DataFrame\n    table = df_to_table(df, table)\n\n    # Update the style of the table\n    table.row_styles = ["none", "dim"]\n    table.box = box.SIMPLE_HEAD\n\n    console.print(table)\n\n```',
    'author': 'Avi Perl',
    'author_email': 'avi@aviperl.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/avi-perl/rich_tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
