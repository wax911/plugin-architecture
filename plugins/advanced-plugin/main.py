from logging import Logger
from random import randint
from time import sleep
from typing import Optional

from engine import PluginCore
from model import Meta, Device


class AdvanceSamplePlugin(PluginCore):

    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)
        self.meta = Meta(
            name='Advanced Sample Plugin',
            description='Advanced Sample plugin template',
            version='0.0.1'
        )

    @staticmethod
    def __simulate_operation() -> None:
        sleep_duration = randint(1, 100) / 100
        sleep(sleep_duration)

    def __get_firmware(self) -> int:
        self._logger.debug('Enquiring device firmware')
        self.__simulate_operation()
        return 0xf41c3e

    def __get_protocol(self) -> str:
        self._logger.debug('Enquiring messaging protocol')
        self.__simulate_operation()
        return "ASCII"

    def __get_errors(self) -> [int]:
        self._logger.debug('Enquiring device errors')
        self.__simulate_operation()
        return [0x2f3a6c, 0xa8e1f5]

    def __create_device(self) -> Device:
        firmware = self.__get_firmware()
        protocol = self.__get_protocol()
        errors = self.__get_errors()

        return Device(
            name='Advanced Sample Device',
            firmware=firmware,
            protocol=protocol,
            errors=errors
        )

    def invoke(self, command: chr, protocol: Optional[str] = None) -> Device:
        self._logger.debug(f'Command: {command} -> {self.meta}')
        device = self.__create_device()
        if device.protocol != protocol:
            self._logger.warning(f'Device does not support protocol supplied protocol')
        return device
