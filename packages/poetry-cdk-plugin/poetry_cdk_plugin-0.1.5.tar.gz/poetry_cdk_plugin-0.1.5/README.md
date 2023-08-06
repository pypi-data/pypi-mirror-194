<p align="left">
<a href="https://pypi.org/project/poetry-cdk-plugin/"><img alt="PyPI" src="https://img.shields.io/pypi/v/black"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# Poetry CDK plugin

Provides CDK CLI commands ```synth```, ```deploy``` and ```destroy``` with basic and default options.

This plugin removes the need to manage SHELL commands to perform basic CDK CLI commands.

## Prerequisites

- [CDK CLI](https://docs.aws.amazon.com/cdk/v2/guide/cli.html)
- [Python](https://www.python.org/) ^3.9
- [Poetry](https://python-poetry.org/) ^1.3

## Installation

Use pip to install the package: ```pip install poetry-cdk-plugin```

## Usage

From a valid CDK codebase root directory, where Poetry is used, type:
- ```poetry cdk synth```: to run cdk synth of your CDK application
- ```poetry cdk deploy```: to run cdk deploy of your CDK application (without approval)
- ```poetry cdk destroy```: to run cdk destroy of your CDK application (with force option)


## Roadmap

- Add a ```cdk lambda package``` command to provide a ZIP for [CDK Lambda construct](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/README.html) and its ```from_asset``` feature
