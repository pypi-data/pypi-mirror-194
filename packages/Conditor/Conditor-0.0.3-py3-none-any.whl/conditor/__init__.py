"""Conditor project management package."""

from __future__ import annotations
from typing import Any

import pathlib
import sys
import inspect
import collections.abc
import json

import conditor.project



class Context :
    """Provides an environment to access conditor resources."""

    def __init__(self, parent:Context|None=None, extend_attributes:dict[str|Any]={}) :
        """Initialize new context.

        Args:
            parent:
                Instance of parent context to inherit environment from.
                `None` defines this context as root.
            extend_attributes:
                Dictionary of attributes to extend this context with.
        """
        self._attributes = extend_attributes
        self.parent = parent
        return

    def __str__(self) :
        return repr(self)
    def __repr__(self) :
        return f'{type(self).__name__}({self.attributes})'

    @property
    def attributes(self) -> dict :
        """Dictionary of all context attributes (inheriting from parent conotexts."""
        if self.parent is None :
            return self._attributes
        return {**self.parent.attributes, **self._attributes}

    def append_attribute(self, name:str, value:Any, overwrite:bool=False) :
        """Safely add a new attribute to this context.

        Args:
            name:
                Index name of the new attribute.
            value:
                Value of the new attribute.
            overwrite:
                If the attribute already exists, it will be overwritten.
                NOTE: Does not affect parent context value,
                but prevents parent attribute from being inherited.
        """
        if not overwrite and name in self.attributes :
            return
        self._attributes[name] = value
        return

    def extend_attributes(self, attributes:dict[str|Any], overwrite:bool=False) :
        """Same as with apprnd_attributes, but takes multiple attributes ad NVP."""
        for attribute in attributes :
            self.append_attribute(attribute, attributes[attribute], overwrite)
            pass
        return

    def spawn(self, init_attributes:dict[str|Any]={}) -> Context :
        """Safe way to create a new context.

        Args:
            init_attributes:
                dictionary of initial context attributes.

        Returns:
            New context instance with current as parent.
        """
        return type(self)(self, init_attributes)

    def eval(self, eval_str:str) -> Any :
        """Perform an eval operation on the given string with this environment as locals.

        Args:
            eval_str:
                String to perform eval on.

        Returns:
            Return value of given eval string.
        """
        return eval(eval_str, globals(), self)

    def __getitem__(self, name) :
        return self.attributes[name]
    def __setitem__(self, name, value) :
        self.append_attribute(name, value, True)
        return
    def __delitem__(self, name) :
        return
    def __iter__(self) :
        return iter(self.attributes)
    def __len__(self) :
        return len(self.attributes)

    pass


def init_base_context() -> Context :
    """Initializes the default conditor root context.

    TODO:
        Implement conditor internals.

    Return:
        Default conditor root context.
    """
    ctx = Context()
    ctx['I'] = 'CONDITOR STUFF'
    return ctx
base_context = init_base_context()
"""Contains the instance of the default conditor root context."""


def get_ctx(search_path:pathlib.Path|None=None) -> Context :
    """Build a context instance at the given path.

    Args:
        search_path:
            Path from which to search for project or build.
            `None` uses strack trace to find the call location of this function.

    Return:
        Context at given location.
    """
    ctx = None
    if search_path is None :
        search_path = inspect.stack(1)[1].filename
        pass
    search_path = pathlib.Path(search_path).absolute()
    project = conditor.project.find_project(search_path)
    if project is None :
        ctx = Context()
        ctx['__CWD__'] = search_path
        return ctx
    build = project.build.find_build(search_path)
    if build is None :
        ctx = project.context
        ctx['__CWD__'] = search_path
        return ctx
    ctx = build.context
    ctx['__CWD__'] = search_path
    return ctx

def __getattr__(name) :
    if name == 'ctx' :
        call_location = inspect.stack(1)[1].filename
        return get_ctx(call_location)
    return



def _ctx_get(module) :
    call_location = inspect.stack(1)[1].filename
    project = conditor.project.find_project(call_location)
    print(project)
    print(project.build.find_build_path(call_location))
    return 'HERE' #conditor.environment.Environment(call_location)
def _ctx_set(module, value) :
    return
def _ctx_del(module) :
    return
_ctx_doc = """Simple environment access at call location."""
def _ctx_init() :
    """Initializes simple environment access."""

    # Create simple environment access property.
    ctx_prop = property(_ctx_get, _ctx_set, _ctx_del, _ctx_doc)

    # Get conditor module instance.
    conditor_module = sys.modules[__name__]

    # Create mutable module class.
    class _mutable_conditor_module (conditor_module.__class__) :
        pass
    conditor_module.__class__ = _mutable_conditor_module

    # Set environment property.
    setattr(conditor_module, 'ctx', ctx_prop)
    setattr(conditor_module.__class__, 'ctx', ctx_prop)

    return
#_ctx_init()
