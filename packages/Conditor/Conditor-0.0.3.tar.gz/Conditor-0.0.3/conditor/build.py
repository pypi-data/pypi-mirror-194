import collections.abc
import json
import importlib
import importlib.util
import sys
import shutil
import pathlib
import re

import conditor


class BuildManager (collections.abc.Mapping) :
    """Interaction with project actions."""
    def __init__(self, project) :
        super().__init__()
        self.project = project
        """Reference to project instance."""
        self.build_cache = {}
        """List of value entries."""
        return
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.project)})'

    def __getitem__(self, name) :
        return Build(self, name)
    def __iter__(self) :
        return iter([])
    def __len__(self) :
        return 0

    @property
    def path(self) :
        """Location of build storage directory."""
        return self.project.path.joinpath('./builds').resolve()

    def new_build(self, name, overwrite=False) :
        build = Build(self, name)
        if build.path.exists() and overwrite :
            shutil.rmtree(build.path)
            pass
        build['__name__'] = name
        return build

    def find_build_path(self, search_path) :
        search_path = pathlib.Path(search_path).absolute()
        if search_path == self.project.path :
            return None
        if search_path == pathlib.Path(search_path.root) :
            return None
        if search_path.is_dir() :
            for node in search_path.iterdir() :
                if node.name == 'properties.json' :
                    return search_path
                pass
            pass
        return self.find_build_path(search_path.parent)

    def find_build(self, search_path) :
        build_path = self.find_build_path(search_path)
        if build_path is None :
            return None
        return self[build_path.name]

    pass

class Build (collections.abc.MutableMapping):
    def __new__(cls, build_manager, name) :
        if name in build_manager.build_cache :
            return build_manager.build_cache[name]
        build = super().__new__(cls)
        build_manager.build_cache[name] = build
        return build
    def __init__(self, build_manager, name) :
        self.build_manager = build_manager
        """Reference to configuration manager."""
        self.name = name
        """Name of this configuration entry."""
        self._context = None
        return
    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.name)})'

    def get(self, name, fallback=None, store_fallback=False) :
        """Get a build property. if not defined, fallback to given value."""
        if name in self :
            return self[name]
        if store_fallback :
            self[name] = fallback
        return fallback

    @property
    def context(self) :
        if self._context is None :
            self._context = self.project.context.spawn()
            self._context['T'] = self
        return self._context
    
    @property
    def project(self) :
        return self.build_manager.project

    #recipe prop
    @property
    def recipe(self) :
        if '__recipe__' not in self :
            return None
        recipe_name = self['__recipe__']
        recipe = self.project.recipe[recipe_name[0]][recipe_name[1]]
        return recipe
    @recipe.setter
    def recipe(self, recipe) :
        recipe_name = recipe.full_name
        self['__recipe__'] = recipe_name
        return

    def __contains__(self, prop_name) :
        if re.fullmatch('^\_.*', prop_name) :
            return prop_name in self.local_props
        return prop_name in self.props
    def __getitem__(self, prop_name) :
        if re.fullmatch('^\_.*', prop_name) :
            return self.local_props[prop_name]
        return self.props[prop_name]
    def __setitem__(self, prop_name, prop_value) :
        props = self.read_props_dict()
        props[prop_name] = prop_value
        self.write_props_dict(props)
        return
    def __delitem__(self, name) :
        return
    def __iter__(self) :
        return iter(self.read_props_dict())
    def __len__(self) :
        return len(self.read_props_dict)

    @property
    def props(self) :
        props = {
            **self.get_base_props(),
            **self.read_props_dict(),
            **self.get_extend_props()
        }
        return props
    @property
    def local_props(self) :
        return self.read_props_dict()

    def get_base_props(self) :
        if '__propbase_build__' in self.read_props_dict() :
            return self.build_manager[self.read_props_dict()['__propbase_build__']].local_props
        return {}
    def get_extend_props(self) :
        if '__propextend_build__' in self.read_props_dict() :
            return self.build_manager[self.read_props_dict()['__propextend_build__']].local_props
        return {}

    @property
    def path(self) :
        return self.build_manager.path.joinpath(f'./{self.name}/').resolve()
    @property
    def props_path(self) :
        return self.path.joinpath(f'./properties.json').resolve()

    def read_props_str(self) :
        if self.props_path.exists() :
            return self.props_path.read_text()
        return ''
    def write_props_str(self, props_str) :
        self.props_path.parent.mkdir(parents=True, exist_ok=True)
        self.props_path.touch(exist_ok=True)
        self.props_path.write_text(props_str)
        return
    def read_props_dict(self) :
        if self.props_path.exists() :
            return json.loads(self.read_props_str())
        return {}
    def write_props_dict(self, props_dict) :
        self.write_props_str(json.dumps(props_dict))
        return

    def stage_all(self, flavour='f') :
        return self.recipe.run_all_stages(self, flavour)

    pass


