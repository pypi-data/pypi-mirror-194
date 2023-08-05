# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_cdk_plugin']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.3,<2.0']

entry_points = \
{'poetry.application.plugin': ['cdk = '
                               'poetry_cdk_plugin.plugin:CDKApplicationPlugin']}

setup_kwargs = {
    'name': 'poetry-cdk-plugin',
    'version': '0.1.1',
    'description': 'CDK commands for Poetry',
    'long_description': '# poetry-cdk-plugin',
    'author': 'Olivier Schmitt',
    'author_email': 'ursusossforever@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/olivier-schmitt/poetry-cdk-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
