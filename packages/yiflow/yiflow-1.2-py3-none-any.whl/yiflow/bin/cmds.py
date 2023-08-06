# -*- encoding: utf-8 -*-
"""
@File        : stage.py
@Description : This script contains the entry point of the package.
@Date        : 2023/02/27 22:14:48
@Author      : merlinbao
@Version     : 1.0
"""

import click

from . import create


@click.group()
def cli():
    pass


@cli.command()
@click.argument('name', nargs=1)
@click.option('-m', '--model_dir', type=str, default=None, help='[optional] Directory where your models are.')
def new(name, model_dir):
    create.main(name, model_dir)


@cli.command()
@click.option('-n', '--name')
def greet(name):
    print(name)


if __name__ == '__main__':
    cli()
