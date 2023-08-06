# -*- encoding: utf-8 -*-
"""
@File        : stage.py
@Description : This module contains the implementation of the ConfigReader class.
@Date        : 2023/02/27 22:14:48
@Author      : merlinbao
@Version     : 1.0
"""

import imp
import json
import os
from pathlib import Path
from typing import Dict

from ..utils import general_funcs


class ConfigReader:

    def __init__(self, config_file):
        """ConfigReader负责配置文件的读取，并将用户写好的Stage类载入环境中

        Args:
            config_file (str): 配置文件的路径
        """

        assert config_file is not None and config_file.endswith('.py'), "Config file is invalid."

        self.load_config(config_file)
        self.register_stages()

    def load_config(self, config_file):
        # 使用项目环境修复路径
        content = None
        with open(config_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                lines[i] = line.replace('$YF_PROJ_PATH', general_funcs.get_proj_dir())
            content = ''.join(lines)

        try:
            self.config = eval(content)
        except SyntaxError:
            raise SyntaxError("Config file is invalid.")

    def register_stages(self):
        stages_dir_path = Path(general_funcs.get_proj_dir()) / 'project' / 'stages'
        assert stages_dir_path.exists(), "Stages are not defined!"

        for stage_path in stages_dir_path.glob('*.py'):
            if 'stage' in str(stage_path):
                _ = imp.load_source(stage_path.name, str(stage_path))

    def get_flows(self) -> Dict[str, Dict]:
        flow_dict = {}
        for k, v in self.config.items():
            if 'flow' in k:
                flow_dict[k] = v
        return flow_dict

    def __str__(self):
        main_str = ''
        main_str += general_funcs.wrap_title("Flow configuration:") + '\n'
        dump_str = json.dumps(self.config, indent=4)
        # dump_str = utils.make_list_flat(dump_str, ['classes'])
        return main_str + dump_str
