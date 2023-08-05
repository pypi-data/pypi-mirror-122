import os
import re
from pathlib import Path
from shutil import copyfile
from typing import Dict, Union, List, Match, TypeVar, Type

import yaml
from fontawesome import icons
from i3ipc.aio import Con
from xdg import BaseDirectory

POSSIBLE_SWAY_CONFIG_PATHS = ['sway', 'i3']

CONFIG_FILE_NAME = 'sdn-config.yaml'

DEFAULT_DELIMITER = " "
DEFAULT_DEFAULT_ICON = "dot-circle"

WINDOW_IDENTIFIERS = ('name', 'window_title', 'window_instance', 'window_class', 'app_id')


class ConfigException(Exception):
    pass


class RuntimeConfigException(Exception):
    pass


T = TypeVar('T')


class ClientConfig:
    def __init__(self, key: str, data: Union[str, Dict], default: Union[str, Dict] = None):
        if default is None:
            default = {}
        self.key = key
        self.extra = None
        if type(data) == str:
            data = {'icon': data}

        if type(data) != dict:
            raise ConfigException(f'clients/{key}: invalid entity {data}')

        self.data = {**default, **data}
        raw_icon = self._get_with_type('icon', str)
        self.icon: str = icons.get(raw_icon, raw_icon)

        self.extra: str = self._get_with_type('extra', str, allow_none=True)

        self.new_desktop = self._get_with_type('new_desktop', bool, allow_none=True)

    def _get_with_type(self, attr: str, expected: Type[T], default=None, allow_none=False) -> T:
        value = self.data.get(attr, default)
        if type(value) == expected or (value is None and allow_none):
            return value
        raise ConfigException(f'clients/{self.key}/{attr}: invalid value {value}')

    def _match(self, leaf: Con):
        for identifier in WINDOW_IDENTIFIERS:
            name = getattr(leaf, identifier, None)
            if name is None:
                continue
            match = re.match(self.key, name, re.IGNORECASE)
            if match:
                return match, name, identifier
        return None, None, None

    def match(self, leaf: Con) -> Match[str]:
        match, name, identifier = self._match(leaf)
        return match

    def match_identity(self, leaf: Con):
        match, name, identifier = self._match(leaf)
        return name, identifier

    def get_symbol(self, leaf: Con, match: Match[str]):
        return Symbol(self, leaf, match)


class Symbol:
    def __init__(self, conf: ClientConfig, leaf: Con, match: Match[str]):
        self.conf = conf
        self.leaf = leaf
        self.match = match

        self.icon = self.format_str(self.conf.icon)
        self.extra = self.format_str(self.conf.extra) if self.conf.extra else None

    def format_str(self, value: str):
        d = {k: getattr(self.leaf, k, None) for k in WINDOW_IDENTIFIERS}
        try:
            return value.format(*self.match.groups(), **d)
        except IndexError:
            raise RuntimeConfigException(
                f"error formatting {value} with numbered values {self.match.groups()} and named values {d}")

    def get(self, workspaces_symbols: List[List["Symbol"]]):
        if self.extra is not None:
            for symbols in workspaces_symbols:
                for symbol in symbols:
                    if symbol.icon == self.icon:
                        return f"{self.icon} {self.extra}"
        return self.icon


class Config:
    _client_configs: Dict[str, ClientConfig] = {}
    _delimiter: str = "|"
    _last_modified: float = None

    def __init__(self, use_default=False):
        self.config_location = Config._find_config() if not use_default else Config._default_config_path()
        print(f"Using config file at {self.config_location}")

    def _load(self):
        if os.path.getmtime(self.config_location) != self._last_modified:
            with open(self.config_location, 'r') as f:
                data = yaml.safe_load(f)
            self._last_modified = os.path.getmtime(self.config_location)

            default_client_config = data.get('default', {})

            self._client_configs = {k: ClientConfig(k, v, default_client_config) for k, v in
                                    data.get('clients', {}).items()}
            self._delimiter = data.get('deliminator', DEFAULT_DELIMITER)

            self._default_icon = data.get('default_icon', DEFAULT_DEFAULT_ICON)
            self._default_icon = icons.get(self._default_icon, self._default_icon)

    @property
    def client_configs(self):
        self._load()
        return self._client_configs

    @property
    def delimiter(self):
        self._load()
        return self._delimiter

    @property
    def default_icon(self):
        self._load()
        return self._default_icon

    @staticmethod
    def _find_config():
        for possible_path in [pp.joinpath(CONFIG_FILE_NAME) for pp in Config._find_sway_folders()]:
            if possible_path.exists():
                return possible_path
        return Config._create_config(Config._find_sway_folders()[0].joinpath(CONFIG_FILE_NAME))

    @staticmethod
    def _find_sway_folders():
        config_base = Path(BaseDirectory.xdg_config_home)
        possible_paths = [config_base.joinpath(pp) for pp in POSSIBLE_SWAY_CONFIG_PATHS]
        return [pp for pp in possible_paths if pp.exists()]

    @staticmethod
    def _create_config(config_location: Path):
        print(f"Creating default config file at {config_location}")
        copyfile(Config._default_config_path(), config_location)
        return config_location

    @staticmethod
    def _default_config_path():
        return Path(os.path.realpath(__file__)).parent.joinpath('default.yaml')
