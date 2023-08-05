<p align="left">
<a href="https://pypi.org/project/poetry-cdk-plugin/"><img alt="PyPI" src="https://img.shields.io/pypi/v/black"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# Poetry CDK plugin

Provides CDK CLI commands ```synth```, ```deploy``` and ```destroy``` with basic and default options.

This plugin removes the need to manage SHELL commands to perform basic CDK CLI commands.

## Prerequisites

- Python ^3.9
- Poetry ^1.3

## Installation

Use pip to install the package: ```pip install poetry-cdk-plugin```

## Usage

From a valid CDK codebase root directory, where Poetry is used, type:
- ```poetry cdk synth```: to run cdk synth of your CDK application
- ```poetry cdk deploy```: to run cdk deploy of your CDK application (without approval)
- ```poetry cdk destroy```: to run cdk destroy of your CDK application (with force option)
