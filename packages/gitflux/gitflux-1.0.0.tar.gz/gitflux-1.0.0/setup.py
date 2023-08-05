# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gitflux', 'gitflux.commands', 'gitflux.providers']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pygithub>=1.55,<2.0']

entry_points = \
{'console_scripts': ['gitflux = gitflux.__main__:cli']}

setup_kwargs = {
    'name': 'gitflux',
    'version': '1.0.0',
    'description': 'A nested command-line utility that helps you manage repositories hosted on Git service providers.',
    'long_description': '# gitflux\n\nA nested command-line utility that helps you manage repositories hosted on Git\nservice providers.\n\n## License\n\nCopyright (C) 2022 HE Yaowen <he.yaowen@hotmail.com>\n\nThe GNU General Public License (GPL) version 3, see [COPYING](./COPYING).\n',
    'author': 'HE Yaowen',
    'author_email': 'he.yaowen@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<3.12',
}


setup(**setup_kwargs)
