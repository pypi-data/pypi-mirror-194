"""Conditor project configuration module."""

from __future__ import annotations
from typing import Any

import collections.abc
import json
import importlib
import pathlib

import conditor


class ConfigManager (collections.abc.MutableMapping) :
    """Interaction with project configuration."""

    def __init__(self, project, path) :
        super().__init__()
        self.project = project
        """Reference to project instance."""
        self.entry_cache = {}
        """List of cached value entries."""
        self.path = pathlib.Path(path).resolve()
        """Path of configuration entry directory."""
        return

    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.project)})'

    def __contains__(self, name) :
        return Entry(self, name).exists
    def __getitem__(self, name) :
        return Entry(self, name).value.get()
    def __setitem__(self, name, value) :
        entry = Entry(self, name)
        if type(value) == tuple and issubclass(value[0], Value) :
            entry.type = value[0]
            value = value[1]
            pass
        else :
            entry.type = LiteralValue
            pass
        entry.value.set(value)
        return
    def __delitem__(self, name) :
        return
    def __iter__(self) :
        return iter(self.list_entry_names())
    def __len__(self) :
        return len(self.list_entry_names())

    def list_entry_names(self, base_path=None) :
        """Generates a list of all configuration entry paths."""
        if base_path is None :
            base_path = self.path
            pass
        if not base_path.exists() :
            return []
        names = []
        for child in base_path.iterdir() :
            if child.suffix == '.json' :
                relpath = str(child.with_suffix('').relative_to(self.path))
                names.append(relpath.replace('/', '.'))
                continue
            if child.is_dir() :
                names.extend(self.list_entry_names(child))
                continue
            pass
        return names

    #@property
    #def path(self) :
    #    """Location of configuration entries directory."""
    #    return self.project.path.joinpath('./_config').resolve()

    pass

class GlobalConfigManager (ConfigManager) :
    def __init__(self, project) :
        super().__init__(project, project.path.joinpath('./.__conditor_config__'))
        return
    pass

class LocalConfigManager (collections.abc.Mapping) :
    @classmethod
    def has_config_at_path(cls, path) :
        config_path = pathlib.Path(path).joinpath('./.__conditor_config__').resolve()
        return config_path.exists()
    def __init__(self, project) :
        self.project = project
        self.cfgmgr_cache = {}
        return
    #def __contains__(self, name) :
    #    print('HERE')
    #    return True
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.project)})'
    def __getitem__(self, relpath) :
        path = self.project.path.joinpath(relpath).resolve()
        index = str(path.relative_to(self.project.path))
        if index not in self.cfgmgr_cache :
            self.cfgmgr_cache[index] = ConfigManager(self.project, path.joinpath('./.__conditor_config__').resolve())
            pass
        return self.cfgmgr_cache[index]
    def __iter__(self) :
        return iter([])
    def __len__(self) :
        return 0

    def list_locals_relpaths(self) :
        """Interates all child directories and returns a list of all local config spaces."""
        return []

    pass


class Entry (collections.abc.MutableMapping) :
    """Represents a configuration entry."""
    def __new__(cls, config_manager, index) :
        if index in config_manager.entry_cache :
            return config_manager.entry_cache[index]
        entry = super().__new__(cls)
        config_manager.entry_cache[index] = entry
        return entry
    def __init__(self, config_manager, index) :
        self.config_manager = config_manager
        """Reference to configuration manager."""
        self.index = index
        """Name of this configuration entry."""
        self._value = None
        """Initialized value instance of this entry."""
        return
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.index)})'
    # tupe mod|class

    def __getitem__(self, name) :
        return self.read_dict()[name]
    def __setitem__(self, name, value) :
        data_dict = self.read_dict()
        data_dict[name] = value
        self.write_dict(data_dict)
        return
    def __delitem__(self, name) :
        return
    def __iter__(self) :
        return iter(self.read_dict())
    def __len__(self) :
        return len(self.read_dict())
    @property
    def project(self) :
        return self.config_manager.project

    @property
    def value(self) :
        if self._value is None :
            self._value = self.type(self)
            pass
        return self._value

    @property
    def type(self) :
        if '__type__' not in self :
            return Value
        cls_module_name, cls_name = self['__type__']
        cls_module = importlib.import_module(cls_module_name)
        cls = getattr(cls_module, cls_name)#fallback return
        return cls
    @type.setter
    def type(self, cls) :
        self['__type__'] = (str(cls.__module__), str(cls.__name__))
        return

    @property
    def relative_path(self) :
        """Composes a relative path to this entry."""
        path = self.index.replace('.', '/')
        return f'{path}.json'
    @property
    def path(self) :
        """Path to this configuration entry."""
        return self.config_manager.path.joinpath(self.relative_path).resolve()
    @property
    def exists(self) :
        return self.path.exists()
    def touch(self) :
        """ensures this entry file exists."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        return

    def read_str(self) :
        """Read string from this data file."""
        if not self.exists :
            return ''
        return self.path.read_text()
    def write_str(self, str_write) :
        """Write string to this data file."""
        self.touch()
        self.path.write_text(str_write)
        return

    def read_dict(self) :
        """Read dictionary from this data file."""
        if not self.exists :
            return {}
        return json.loads(self.read_str())
    def write_dict(self, dict_write) :
        """Write dictionary to this data file."""
        self.write_str(json.dumps(dict_write))
        return

    pass


class Value :
    """Represents a value instance of an entry."""
    def __init__(self, entry) :
        self.entry = entry
        """Reference to value entry."""
        return
    @property
    def project(self) :
        return self.entry.project
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.entry)})'
    def get(self) :
        return 'UNDEFINED'
    def set(self, value) :
        return '?'
    pass

class LiteralValue (Value) :
    """Represents a literal value."""
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        return
    def get(self) :
        return eval(self.entry['value'])
    def set(self, value) :
        self.entry['value'] = repr(value)
        return
    pass

class FormatString (Value) :
    """Represents a formated string.

    TODO:
        Maybe use stack trace to get context? (Suppport to format in build instance).
    """
    def get(self) :
        raw_str = self.entry['raw_str']
        form_str = conditor.compose.exec_format(raw_str, self.project.context)
        # TODO if local get build
        return form_str
    def set(self, value) :
        self.entry['raw_str'] = value
        return

