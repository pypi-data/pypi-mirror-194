# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polario']

package_data = \
{'': ['*']}

install_requires = \
['fsspec>=2023.1.0,<2024.0.0',
 'polars>=0.16.8,<0.17.0',
 'pyarrow>=11.0.0,<12.0.0']

setup_kwargs = {
    'name': 'polario',
    'version': '0.1.0',
    'description': 'Polars IO',
    'long_description': 'Polars IO utility library\n=================\n\nHelpers to make it easier to read and write Hive partitioned parquet dataset with Polars.\n\n\nDataset\n=======\nExample of use of `polario.dataset.HiveDataset`\n```python\n\nfrom polario.dataset import HiveDataset\nimport polars as pl\ndf = pl.from_dicts(\n        [\n            {"p1": 1, "v": 1},\n            {"p1": 2, "v": 1},\n        ]\n    )\n\nds = HiveDataset("file:///tmp/", partition_columns=["p1"])\n\nds.write(df)\n\nfor partition_df in ds.read_partitions():\n    print(partition_df)\n\n```',
    'author': 'Bram Neijt',
    'author_email': 'bram@neijt.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bneijt.github.io/polario/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
