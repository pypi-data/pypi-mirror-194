# -*- encoding: utf-8 -*-
"""
@File        : stage.py
@Description : This module contains the base class for all interfaces.
@Date        : 2023/02/27 22:14:48
@Author      : merlinbao
@Version     : 1.0
"""


from abc import ABC, abstractmethod
from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict

from ..tools import ConfigReader
from ..utils import get_proj_dir
from .flow import Flow


class Interface(ABC):

    def __init__(self, config_file=None, flow_name=None, **kwargs):
        # Get global settings
        setting_dict = self._get_default_settings()
        print(setting_dict)
        if config_file == None:
            config_file = setting_dict["config_file"]

        # Read config file
        cfg_reader = ConfigReader(config_file)

        # Show config
        if setting_dict["print_config"]:
            print(cfg_reader)

        # Initialize flows
        flow_config_dict = cfg_reader.get_flows()
        for name, config in flow_config_dict.items():
            # Only initialize the flow with the given name
            if flow_name is not None and name != flow_name:
                continue

            flow = Flow.from_config(config=config)
            setattr(self, name, flow)

    def _get_default_settings(self) -> Dict[str, Any]:
        setting_file_path = Path(get_proj_dir()) / 'settings.ini'
        assert setting_file_path.exists(), "Default setting file is not provided!"

        setting = ConfigParser()
        setting.read(str(setting_file_path))
    
        # Read default config file
        config_file_path = Path(get_proj_dir()) / 'project' / setting['project'].get("config")

        # Read flag if print config
        print_config = setting["project"].getboolean("print_config")

        return dict(config_file=str(config_file_path), print_config=print_config)
