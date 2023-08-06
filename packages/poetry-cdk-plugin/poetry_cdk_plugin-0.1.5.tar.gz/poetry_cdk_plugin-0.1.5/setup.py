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
    'version': '0.1.5',
    'description': 'CDK commands for Poetry',
    'long_description': '<p align="left">\n<a href="https://pypi.org/project/poetry-cdk-plugin/"><img alt="PyPI" src="https://img.shields.io/pypi/v/black"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\n# Poetry CDK plugin\n\nProvides CDK CLI commands ```synth```, ```deploy``` and ```destroy``` with basic and default options.\n\nThis plugin removes the need to manage SHELL commands to perform basic CDK CLI commands.\n\n## Prerequisites\n\n- [CDK CLI](https://docs.aws.amazon.com/cdk/v2/guide/cli.html)\n- [Python](https://www.python.org/) ^3.9\n- [Poetry](https://python-poetry.org/) ^1.3\n\n## Installation\n\nUse pip to install the package: ```pip install poetry-cdk-plugin```\n\n## Usage\n\nFrom a valid CDK codebase root directory, where Poetry is used, type:\n- ```poetry cdk synth```: to run cdk synth of your CDK application\n- ```poetry cdk deploy```: to run cdk deploy of your CDK application (without approval)\n- ```poetry cdk destroy```: to run cdk destroy of your CDK application (with force option)\n\n\n## Roadmap\n\n- Add a ```cdk lambda package``` command to provide a ZIP for [CDK Lambda construct](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/README.html) and its ```from_asset``` feature\n',
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
