from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PluginRunTimeOption(object):
    main: str
    tests: Optional[List[str]]


@dataclass
class DependencyModule:
    name: str
    version: str

    def __str__(self) -> str:
        return f'{self.name}=={self.version}'


@dataclass
class PluginConfig:
    name: str
    alias: str
    creator: str
    runtime: PluginRunTimeOption
    repository: str
    description: str
    version: str
    requirements: Optional[List[DependencyModule]]


@dataclass
class Meta:
    name: str
    description: str
    version: str

    def __str__(self) -> str:
        return f'{self.name}: {self.version}'


@dataclass
class Device:
    name: str
    firmware: int
    protocol: str
    errors: List[int]
