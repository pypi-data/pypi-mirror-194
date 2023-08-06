"""Build recipe module."""

import collections.abc
import json
import importlib
import importlib.util
import sys

import conditor


class RecipeManager (collections.abc.Mapping) :
    """Interaction with project recipes."""
    def __init__(self, project) :
        super().__init__()
        self.project = project
        """Reference to project instance."""
        self.entry_cache = {}
        """List of value entries."""
        return
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.project)})'

    def __getitem__(self, location) :
        return Entry(self, location)
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
        # TODO: import recipes return?
        return iter(self.list_path_entries())
    def __len__(self) :
        return len(self.list_path_entries())

    def list_path_entries(self) :
        """Composes a list of recipe file entries."""
        entries = []
        for node in self.path.iterdir() :
            if node.is_file() and node.suffix == '.py' :
                entries.append(node.with_suffix('').name)
                pass
            pass
        return entries

    @property
    def path(self) :
        """Location of recipe entries directory."""
        return self.project.path.joinpath('./.__conditor_recipes__').resolve()

    def import_recipe(self, location) :
        """Import a recipe from module."""
        __import__(location)
        return ImportEntry(self, location)

    pass

class Entry (collections.abc.Mapping):
    def __new__(cls, recipe_manager, index) :
        if index in recipe_manager.entry_cache :
            return recipe_manager.entry_cache[index]
        entry = super().__new__(cls)
        recipe_manager.entry_cache[index] = entry
        return entry
    def __init__(self, recipe_manager, location) :
        self.recipe_manager = recipe_manager
        """Reference to configuration manager."""
        self.location = location
        """Name of this configuration entry."""
        self.recipe_cache = {}
        self._module = None
        """Initialized value instance of this entry."""
        return
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.location)})'

    def __getitem__(self, recipe_name) :
        if recipe_name not in self.recipe_cache :
            self.recipe_cache[recipe_name] = getattr(self.module, recipe_name)(self)
            pass
        return self.recipe_cache[recipe_name]
    def __iter__(self) :
        return iter(self.list_class_names())
    def __len__(self) :
        return len(self.list_class_names())

    def list_class_names(self) :
        """Compses a list of recipe class names in this entry module."""
        class_names = []
        for class_name in self.module.__dict__ :
            if issubclass(self.module.__dict__[class_name], Recipe) :
                class_names.append(class_name)
                pass
            pass
        return class_names

    @property
    def project(self) :
        return self.recipe_manager.project
    @property
    def relpath(self) :
        # TODO: remove and only use path.
        return f'./{self.location}.py'
    @property
    def path(self) :
        # TODO: handle module import recipes.
        return self.recipe_manager.path.joinpath(self.relpath).resolve()

    @property
    def module_name(self) :
        return f'conditor.recipe.__loaded_recipes__.{self.location}'

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
        """Default recipe class."""
        return self[self.module.DEFAULT_RECIPE]

    pass


class ImportEntry (Entry) :
    @property
    def module_name(self) :
        return self.module.__name__
    @property
    def module(self) :
        __import__(self.location)
        return sys.modules[self.location]
    pass


class Recipe :
    """Recipe superclass."""
    STAGES = []
    NAME = '__UNNAMED__'
    def __init__(self, entry) :
        self.entry = entry
        return
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.entry.path)})'
    #@property
    #def stages(self) :
    #    stages = []
    #    for stage_name in type(self).STAGES :
    #        stages.append(getattr(self, stage_name))
    #        pass
    #    return stages
    @property
    def full_name(self) :
        return (self.entry.location, type(self).__name__)
    @property
    def project(self) :
        return self.entry.recipe_manager.project
    def new_build(self, identity='UNDEFINED_IDENTITY') :
        name = f'{type(self).NAME}-{identity}'
        build = self.project.build.new_build(name, overwrite=True)
        build.recipe = self
        return build
    def get_stage_name(self, name) :
        return getattr(self, name)
    def run_stage_name(self, build, name, flavour='FLAVOUR') :
        stage = self.get_stage_name(name)
        stage_return = stage(build, flavour)
        #current running flag
        return stage_return
    def run_stage_index(self, build, index, flavour='FLAV') :
        stage_name = type(self).STAGES[index]
        return self.run_stage_name(build, stage_name, flavour)
    def run_next_stage(self, build, flavour='FLAVVVVV') :
        if '__index__' not in build :
            build['__index__'] = 0
            pass
        if build['__index__'] == -1 :
            return -1
        if build['__index__'] == len(type(self).STAGES) :
            build['__index__'] = -1
            return -1
        self.run_stage_index(build, build['__index__'], flavour)
        if build['__index__'] + 1 >= len(type(self).STAGES) :
            build['__index__'] = -1
            return -1
        build['__index__'] = build['__index__'] + 1
        return build['__index__']
    def run_all_stages(self, build, flavour='FFFF') :
        while self.run_next_stage(build, flavour) != -1 :
            continue
        return
    pass


class ConditorRecipe (Recipe) :
    STAGES = ['create']
    NAME = '__UNNAMED_CONDITOR__'
    def create(self) :
        return
    pass

