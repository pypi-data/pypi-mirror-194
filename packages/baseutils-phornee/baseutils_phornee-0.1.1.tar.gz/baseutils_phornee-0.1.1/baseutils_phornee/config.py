import os
import yaml
import copy
from pathlib import Path

import logging

log = logging.getLogger(__name__)

class Config:
    """ Manages a config file that will be generated in the /var/ folder
    """

    def __init__(self, package_name: str, template_path: str, config_file_name: str):
        """_summary_

        Args:
            package_name (str): Name of the package owner of the config file
            template_path (str): Path of the template file
            config_path (str): Name of config file (will be placed in home/var/{modulename} folder)
        """
        self._template_path = template_path
        self._config_file_name = config_file_name
        self.homevar = os.path.join(str(Path.home()), 'var', package_name)

        if not os.path.exists(self.homevar):
            os.makedirs(self.homevar)

        self.config = {}

        self._readConfig()

    def __getitem__(self, key):
        return self.config.get(key, None)

    @staticmethod
    def getConfigPath(package_name: str, config_file_name: str) -> str:
        return os.path.join(str(Path.home()), 'var', package_name, config_file_name)

    def getDict(self) -> dict:
        return self.config

    def getDictCopy(self) -> dict:
        return copy.deepcopy(self.config)

    def _readConfig(self):
        # First get default values from template config file
        # config_template_yml_path = os.path.join(self._installfolder, 'config-template.yml')
        config_template_yml_path = self._template_path
        try:
            # First try to get the template
            with open(config_template_yml_path, 'r') as config_template_file:
                template_config = yaml.load(config_template_file, Loader=yaml.FullLoader)
        except OSError as error:
            # No template
            template_config = None

        # Try to get the config
        try:
            config_yml_path = os.path.join(self.homevar, self._config_file_name)
            with open(config_yml_path, 'r') as config_file:
                config = yaml.load(config_file, Loader=yaml.FullLoader)
        except OSError as error:
            config = None

        if config:
            if template_config:
                self._mergeConfig(config, template_config)
                self.config = template_config
            else:
                self.config = config
        else:  # No previous config
            if template_config:  # If config file doesn´t exist, but template does, write config with template content
                self.update(template_config)
                self.write()

    def refresh(self):
        self._readConfig()

    @staticmethod
    def _mergeConfig(source_config, dest_config):
        # if type(source_config) != type(dest_config):
        #     raise Exception('Source and destination configs dont match its data types: {} vs {}'.format(source_config, dest_config))
        #Update keys
        if type(dest_config) == dict:
            for key, value in source_config.items():
                if key not in dest_config:
                    if type(value) == dict:
                        dest_config[key] = {}  
                    elif type(value) == list:
                        dest_config[key] = []
                if type(value) in [int, str]:
                    dest_config[key] = value
                Config._mergeConfig(source_config[key], dest_config[key])      
        elif type(dest_config) == list:
            if type(source_config) != list:
                raise
            for elem in source_config:
                if elem not in dest_config:
                    dest_config.append(elem)
        else:
            dest_config = source_config

    def update(self, config_update):
        # Update keys
        self._mergeConfig(config_update, self.config)

    def write(self):
        config_yml_path = os.path.join(self.homevar, self._config_file_name)
        try:
            with open(config_yml_path, 'w') as config_file:
                yaml.dump(self.config, config_file)
        except OSError as error:
            pass

    def delete(self):
        config_yml_path = os.path.join(self.homevar, self._config_file_name)
        try:
            os.remove(config_yml_path)
        except OSError as error:
            pass
