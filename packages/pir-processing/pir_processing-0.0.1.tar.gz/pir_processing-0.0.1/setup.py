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
    'version': '0.0.1',
    'description': "Python tools for processing ARTA's PIR file format",
    'long_description': "# pir-processing\n\nPython processing tools for ARTA's .pir files.\n\n## Requirements:\n- NumPy ~= 1.22.4\n\n## Instructions\n\nIn order to transform a series of PIR files to TXT, run the tool as follows:\n\n```python3 transform_all_pir_to_ascii PATH_TO_YOUR_PIR_FILES [--csv]```\n\nwhere you need to replace `PATH_TO_YOUR_PIR_FILES` with guess what... the path to your god forsaken PIR files. The `--csv` flag lets you transform them to CSV instead, which includes a synthetic time axis starting at 0 seconds.\n\nYou'll find the output files in the same directory you gave as input.",
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
