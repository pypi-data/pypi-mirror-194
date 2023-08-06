# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tictot', 'tictot.config', 'tictot.db', 'tictot.status', 'tictot.widgets']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'sqlalchemy>=2.0.4,<3.0.0',
 'textual[dev]>=0.12.1,<0.13.0']

entry_points = \
{'console_scripts': ['tictot = tictot.cli:run']}

setup_kwargs = {
    'name': 'tictot',
    'version': '0.1.1',
    'description': '',
    'long_description': "# tictot\n\n![Showcase](https://raw.githubusercontent.com/daniarlert/tictot/master/assets/showcase.gif)\n\n\ntictot is a simple time tracker for the terminal that is easy and fast to use. With tictot you can track the time spent on different tasks and keep a record of your worked hours. The application is built with [textual](https://textual.textualize.io/), an awesome framework for building applications for the terminal.\ntictot is also inspired by the [textual's example application](https://textual.textualize.io/tutorial/).\n\n## Work in progress\n\nFor the moment tictot only supports tracking time for a single task at a time. It also doesn't support tags, categories or any other fancy stuff. Also you can't update past entries or delete them. But I'm working on it.\n\n## Installation\n\n### Using pip\n\n```bash\npip install tictot\n```\n\n### From source\n\n```bash\ngit clone https://github.com/daniarlert/tictot.git\n```\n\nNow, install the application:\n\n```bash\ncd tictot && pip install .\n```\n\n\n## To Do\n\n- [ ] Update past entries.\n- [ ] Delete entries.\n- [ ] Support tags.\n- [ ] Support user configuration.\n- [ ] Statistics.\n",
    'author': 'daniarlert',
    'author_email': 'arlertdaniel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
