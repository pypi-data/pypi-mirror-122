# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['truhanen', 'truhanen.stuiplot']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.0', 'numpy>=1.21.0', 'pandas>=1.3.0']

entry_points = \
{'console_scripts': ['stuiplot = truhanen.stuiplot:main']}

setup_kwargs = {
    'name': 'truhanen.stuiplot',
    'version': '0.1.0',
    'description': 'Script for plotting s-tui logs',
    'long_description': "# stuiplot\n\nScript for plotting s-tui logs.\n\n## Usage\n\n```\n$ stuiplot --help\nusage: stuiplot [-h] [--figure-path FIGURE_PATH] [--align-threshold ALIGN_THRESHOLD] [--minutes MINUTES] log [log ...]\n\nRead s-tui csv log files & plot CPU frequency, temperature, &\nutilization percentage as a function of time. All values shown are\nmeans over all CPU cores.\n\npositional arguments:\n  log                   path to s-tui log file\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --figure-path FIGURE_PATH\n                        if given, don't show the figure but write it to this file\n  --align-threshold ALIGN_THRESHOLD\n                        CPU utilization threshold for aligning the data on the time axis\n  --minutes MINUTES     amount of time to show\n```\n\n## Installation\n\nInstall from PyPI with `pip install truhanen.stuiplot` and from sources with\n`pip install .`.",
    'author': 'Tuukka Ruhanen',
    'author_email': 'tuukka.t.ruhanen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/truhanen/stuiplot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
