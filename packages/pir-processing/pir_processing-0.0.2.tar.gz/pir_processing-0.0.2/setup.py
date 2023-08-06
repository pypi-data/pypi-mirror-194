# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pir_processing', 'pir_processing.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0', 'numpy>=1.24.2,<2.0.0', 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'pir-processing',
    'version': '0.0.2',
    'description': "Python tools for processing ARTA's PIR file format",
    'long_description': "# pir-processing\n\nPython tools for processing ARTA's .pir files.\n\n## Installation\n\n`pip install pir-processing`\n\n## Requirements\n\n`python >=3.8,<3.10`\n\n## Usage\n\nIn order to transform a single PIR file to .txt, run the tool as follows:\n\n```python -m pir_processing --directory PATH_TO_THE_PIR_FILE [--csv]```\n\n\nIn order to transform a series of PIR files to TXT, run the tool as follows:\n\n```python -m pir_processing --directory PATH_TO_YOUR_PIR_FILES [--csv]```\n\nwhere you need to replace `PATH_TO_YOUR_PIR_FILES` with guess what... the path to your god forsaken PIR files.\n\nThe `--csv` flag lets you transform them to CSV instead, which includes a synthetic time axis starting at 0 seconds.\n\n\nThe output files are saved in the same directory that was passed as input.\n",
    'author': 'Ivan Pupkin',
    'author_email': 'ipupkin@untref.edu.ar',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
