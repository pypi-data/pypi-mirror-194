# -*- encoding: utf-8 -*-
"""
@File        : stage.py
@Description : This module contains the base class for all runners.
@Date        : 2023/02/27 22:14:48
@Author      : merlinbao
@Version     : 1.0
"""

from abc import abstractmethod


class Runner(object):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self):
        raise NotImplementedError("`run` method must be implemented!")