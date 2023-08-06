import collections.abc
import json
import importlib
import importlib.util
import sys

import conditor


class ActionManager (collections.abc.Mapping) :
    """Interaction with project actions."""
    def __init__(self, project) :
        super().__init__()
        self.project = project
        """Reference to project instance."""
        self.action_cache = {}
        """List of value entries."""
        return
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.project)})'

    def __getitem__(self, location) :
        if '/' not in location :
            return Entry(self, location).default
        location, action = location.split('/', 1)
        return Entry(self, location)[action]
    #def __setitem__(self, name, value) :
    #    # handle value type
    #    # otherwise literal
    #    # if not value object.
    #    entry = Action(self, location)
    #    entry.type = LiteralValue
    #    entry.value.set(value)
    #    return
    #def __delitem__(self, name) :
    #    return
    def __iter__(self) :
        return iter([])
    def __len__(self) :
        return 0

    @property
    def path(self) :
        """Location of configuration entries directory."""
        return self.project.path.joinpath('./.__conditor_actions__').resolve()

    def import_action(self, location) :
        __import__(location)
        return ImportEntry(self, location)

    pass

class Entry (collections.abc.Mapping):
    def __new__(cls, action_manager, index) :
        if index in action_manager.action_cache :
            return action_manager.action_cache[index]
        entry = super().__new__(cls)
        action_manager.action_cache[index] = entry
        return entry
    def __init__(self, action_manager, location) :
        self.action_manager = action_manager
        """Reference to configuration manager."""
        self.location = location
        """Name of this configuration entry."""
        self.action_cache = {}
        self._module = None
        """Initialized value instance of this entry."""
        return
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.location)})'

    def __getitem__(self, action_name) :
        if action_name not in self.action_cache :
            self.action_cache[action_name] = getattr(self.module, action_name)(self)
            pass
        return self.action_cache[action_name].run
    def __iter__(self) :
        return iter([])
    def __len__(self) :
        return 0

    @property
    def relpath(self) :
        return f'./{self.location}.py'
    @property
    def path(self) :
        return self.action_manager.path.joinpath(self.relpath).resolve()

    @property
    def module_name(self) :
        return f'conditor.action.__loaded_action__.{self.location}'

    @property
    def module(self) :
        if self._module is None :
            if self.module_name not in sys.modules :
                module_spec = importlib.util.spec_from_file_location(self.module_name, self.path)
                sys.modules[self.module_name] = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(sys.modules[self.module_name])
                pass
            self._module = sys.modules[self.module_name]
            pass
        return self._module

    @property
    def default(self) :
        return self[self.module.DEFAULT_ACTION]

    pass

class ImportEntry (Entry) :
    @property
    def module_name(self) :
        return self.module.__name__
    @property
    def module(self) :
        return sys.modules[self.location]
    pass

class Action :
    """Action superclass."""
    def __init__(self, entry) :
        self.entry = entry
        return
    def run(self) :
        print('run this action')
        return
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.entry.path)})'
    pass


