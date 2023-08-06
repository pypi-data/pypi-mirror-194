

from __future__ import annotations
from typing import Any

import pathlib

import conditor
import conditor.config
import conditor.action
import conditor.build
import conditor.recipe
import conditor.compose


def find_project_path(search_path:pathlib.Path) -> pathlib.Path|None :
    """Search a project path in parents of given path.

    Args:
        search_path:
            Path at which to start project root search.

    Returns:
        First found project root path.
        `None` if no project root path was found.
    """
    identifier_file_names = ['.__conditor_project__.json']
    root_path = pathlib.Path(search_path.root).resolve()
    search_path = pathlib.Path(search_path).resolve()
    while not search_path.exists() or search_path.is_file() :
        if search_path == root_path :
            return None
        search_path = search_path.parent
        pass
    while search_path != root_path :
        for child in search_path.iterdir() :
            if child.name in identifier_file_names :
                return search_path
            pass
        search_path = search_path.parent
        pass
    return None

def find_project(search_path:pathlib.Path) -> Project|None :
    """Find a project at given path.

    Args:
        search_path:
            Path at which to start project search.

    Returns:
        Instance of found project.
        `None` if no project root directory was found.
    """
    project_path = find_project_path(search_path)
    if project_path is None :
        return None
    return Project(project_path)


PROJECT_CACHE:dict[str|Project] = {}
"""Initialized project instances indexed by resolved absolute path.

TODO:
    private
"""

class Project :
    """Conditor project instance."""

    def __new__(cls, path) :
        """Get new project instance or retrieve from cache.

        Args:
            path:
                Path within project root.
        """
        path = find_project_path(path)
        if path is None :
            return None
        path = path.resolve()
        if str(path) in PROJECT_CACHE :
            return PROJECT_CACHE[str(path)]
        project = super().__new__(cls)
        PROJECT_CACHE[str(path)] = project
        project.path = path
        """Location of project root directory."""
        project._global_config_manager = None
        """Instance of global config manager."""
        project._local_config_manager = None
        """Instance of local config manager."""
        project._action = None
        """Instance of action manager."""
        project._build = None
        """Instance of build manager."""
        project._recipe = None
        """Instance of recipe manager."""
        project._context = None
        """Instance of project context."""
        return project
    def __init__(self, path) :
        return

    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}(path={repr(self.path)})'

    @property
    def global_config(self) -> conditor.config.GlobalConfigManager :
        """Project global config manager."""
        if self._global_config_manager is None :
            self._global_config_manager = conditor.config.GlobalConfigManager(self)
        return self._global_config_manager

    @property
    def local_config(self) -> conditor.config.LocalConfigManager :
        """Project local config manager."""
        if self._local_config_manager is None :
            self._local_config_manager = conditor.config.LocalConfigManager(self)
        return self._local_config_manager

    @property
    def action(self) -> conditor.action.ActionManager :
        """Project action manager."""
        if self._action is None :
            self._action = conditor.action.ActionManager(self)
            pass
        return self._action

    @property
    def build(self) -> conditor.build.BuildManager :
        """Project build manager."""
        if self._build is None :
            self._build = conditor.build.BuildManager(self)
            pass
        return self._build

    @property
    def recipe(self) -> conditor.recipe.RecipeManager :
        """Project recipe manager."""
        if self._recipe is None :
            self._recipe = conditor.recipe.RecipeManager(self)
            pass
        return self._recipe

    @property
    def context(self) -> conditor.Context :
        """Project context instance."""
        if self._context is None :
            self._context = conditor.base_context.spawn()
            self._context['__PROJECT__'] = self
            self._context['L'] = self.local_config
            self._context['G'] = self.global_config
            self._context['B'] = self.build
            self._context['Q'] = self.recipe
            self._context['A'] = self.action
            pass
        return self._context

    @property
    def G(self) :
        """Global config shortcut."""
        return self.global_config
    @property
    def L(self) :
        """Local config shortcut"""
        return self.local_config
    @property
    def A(self) :
        """Actions shortcut."""
        return self.action
    @property
    def B(self) :
        """Builds shortcut."""
        return self.build

    pass







