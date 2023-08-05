"""
    Facilities for plugin loading and registration.
"""

import importlib
import pkgutil
from functools import lru_cache

import renumics.spotlight.plugins as plugins_namespace


@lru_cache()
def load_plugins() -> dict:
    """
    Automatically load and register plugins
    inside the renumics.spotlight.plugins namespace package.
    """
    plugins = {}

    for _, name, _ in pkgutil.iter_modules(plugins_namespace.__path__):
        plugin = importlib.import_module(plugins_namespace.__name__ + "." + name)
        plugins[name] = plugin

    for plugin in sorted(plugins.values(), key=lambda m: m.__priority__):
        if hasattr(plugin, "__activate__"):
            plugin.__activate__()

    return plugins
