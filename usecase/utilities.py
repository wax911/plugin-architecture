import os
import subprocess
import sys

from logging import Logger
from subprocess import CalledProcessError
from typing import List, Dict, Optional

import pkg_resources
from dacite import from_dict, ForwardReferenceError, UnexpectedDataError, WrongTypeError, MissingValueError
from pkg_resources import Distribution

from model import PluginConfig, DependencyModule
from util import FileSystem


class PluginUtility:
    __IGNORE_LIST = ['__pycache__']

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self._logger = logger

    @staticmethod
    def __filter_unwanted_directories(name: str) -> bool:
        return not PluginUtility.__IGNORE_LIST.__contains__(name)

    @staticmethod
    def filter_plugins_paths(plugins_package) -> List[str]:
        """
        filters out a list of unwanted directories
        :param plugins_package:
        :return: list of directories
        """
        return list(
            filter(
                PluginUtility.__filter_unwanted_directories,
                os.listdir(plugins_package)
            )
        )

    @staticmethod
    def __get_missing_packages(
            installed: List[Distribution],
            required: Optional[List[DependencyModule]]
    ) -> List[DependencyModule]:
        missing = list()
        if required is not None:
            installed_packages: List[str] = [pkg.project_name for pkg in installed]
            for required_pkg in required:
                if not installed_packages.__contains__(required_pkg.name):
                    missing.append(required_pkg)
        return missing

    def __manage_requirements(self, package_name: str, plugin_config: PluginConfig):
        installed_packages: List[Distribution] = list(
            filter(lambda pkg: isinstance(pkg, Distribution), pkg_resources.working_set)
        )
        missing_packages = self.__get_missing_packages(installed_packages, plugin_config.requirements)
        for missing in missing_packages:
            self._logger.info(f'Preparing installation of module: {missing} for package: {package_name}')
            try:
                python = sys.executable
                exit_code = subprocess.check_call(
                    [python, '-m', 'pip', 'install', missing.__str__()],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self._logger.info(
                    f'Installation of module: {missing} for package: {package_name} was returned exit code: {exit_code}'
                )
            except CalledProcessError as e:
                self._logger.error(f'Unable to install package {missing}', e)

    def __read_configuration(self, module_path) -> Optional[PluginConfig]:
        try:
            plugin_config_data = FileSystem.load_configuration('plugin.yaml', module_path)
            plugin_config = from_dict(data_class=PluginConfig, data=plugin_config_data)
            return plugin_config
        except FileNotFoundError as e:
            self._logger.error('Unable to read configuration file', e)
        except (NameError, ForwardReferenceError, UnexpectedDataError, WrongTypeError, MissingValueError) as e:
            self._logger.error('Unable to parse plugin configuration to data class', e)
        return None

    def setup_plugin_configuration(self, package_name, module_name) -> Optional[str]:
        """
        Handles primary configuration for a give package and module
        :param package_name: package of the potential plugin
        :param module_name: module of the potential plugin
        :return: a module name to import
        """
        # if the item has not folder we will assume that it is a directory
        module_path = os.path.join(FileSystem.get_plugins_directory(), module_name)
        if os.path.isdir(module_path):
            self._logger.debug(f'Checking if configuration file exists for module: {module_name}')
            plugin_config: Optional[PluginConfig] = self.__read_configuration(module_path)
            if plugin_config is not None:
                self.__manage_requirements(package_name, plugin_config)
                return plugin_config.runtime.main
            else:
                self._logger.debug(f'No configuration file exists for module: {module_name}')
        self._logger.debug(f'Module: {module_name} is not a directory, skipping scanning phase')
        return None
