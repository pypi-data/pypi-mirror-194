# -*- encoding: utf-8 -*-
"""
@File        : stage.py
@Description : This module contains some basic functions.
@Date        : 2023/02/27 22:14:48
@Author      : merlinbao
@Version     : 1.0
"""

import os
from colorama import Fore, Style


def wrap_title(text):
    return Fore.GREEN + str(text) + Style.RESET_ALL


def wrap_link(text):
    return Fore.RED + str(text) + Style.RESET_ALL


def make_list_flat(string, keys):
    def _flat(string, key):
        new_string = ''
        left, right = 0, 0
        try:
            pos = string.index(key)
            left = pos + string[pos:].index('[')
            right = pos + string[pos:].index(']')
            new_string = string[:left] + string[left:right].replace('\n', '').replace(' ', '').replace(',', ', ')
            new_string += _flat(string[right:], key)
        except ValueError:
            new_string += string[right:]
        return new_string

    for key in keys:
        string = _flat(string, key)

    return string


def get_proj_dir(name=None):
    root_dir = os.getenv('YF_PROJ_PATH').replace('\\', '/')

    if name == None:
        return root_dir
    elif name == "project":
        return os.path.join(root_dir, "project")
    else:
        project_dir = os.path.join(root_dir, "project")
        _, dirs, _ = next(os.walk(project_dir))

        assert name in dirs, "Directory name is not found in `project`"

        return os.path.join(project_dir, name)
