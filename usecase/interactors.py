import os
from importlib import import_module
from logging import Logger
from typing import List, Any, Dict

from engine import IPluginRegistry, PluginCore
from util import LogUtil
from .utilities import PluginUtility


class PluginUseCase:
    _logger: Logger
    modules: List[type]

    def __init__(self, options: Dict) -> None:
        self._logger = LogUtil.create(options['log_level'])
        self.plugins_package: str = options['directory']
        self.plugin_util = PluginUtility(self._logger)
        self.modules = list()

    def __check_loaded_plugin_state(self, plugin_module: Any):
        if len(IPluginRegistry.plugin_registries) > 0:
            latest_module = IPluginRegistry.plugin_registries[-1]
            latest_module_name = latest_module.__module__
            current_module_name = plugin_module.__name__
            if current_module_name == latest_module_name:
                self._logger.debug(f'Successfully imported module `{current_module_name}`')
                self.modules.append(latest_module)
            else:
                self._logger.error(
                    f'Expected to import -> `{current_module_name}` but got -> `{latest_module_name}`'
                )
            # clear plugins from the registry when we're done with them
            IPluginRegistry.plugin_registries.clear()
        else:
            self._logger.error(f'No plugin found in registry for module: {plugin_module}')

    def __search_for_plugins_in(self, plugins_path: List[str], package_name: str):
        for directory in plugins_path:
            entry_point = self.plugin_util.setup_plugin_configuration(package_name, directory)
            if entry_point is not None:
                plugin_name, plugin_ext = os.path.splitext(entry_point)
                # Importing the module will cause IPluginRegistry to invoke it's __init__ fun
                import_target_module = f'.{directory}.{plugin_name}'
                module = import_module(import_target_module, package_name)
                self.__check_loaded_plugin_state(module)
            else:
                self._logger.debug(f'No valid plugin found in {package_name}')

    def discover_plugins(self, reload: bool):
        """
        Discover the plugin classes contained in Python files, given a
        list of directory names to scan.
        """
        if reload:
            self.modules.clear()
            IPluginRegistry.plugin_registries.clear()
            self._logger.debug(f'Searching for plugins under package {self.plugins_package}')
            plugins_path = PluginUtility.filter_plugins_paths(self.plugins_package)
            package_name = os.path.basename(os.path.normpath(self.plugins_package))
            self.__search_for_plugins_in(plugins_path, package_name)

    @staticmethod
    def register_plugin(module: type, logger: Logger) -> PluginCore:
        """
        Create a plugin instance from the given module
        :param module: module to initialize
        :param logger: logger for the module to use
        :return: a high level plugin
        """
        return module(logger)

    @staticmethod
    def hook_plugin(plugin: PluginCore):
        """
        Return a function accepting commands.
        """
        return plugin.invoke
