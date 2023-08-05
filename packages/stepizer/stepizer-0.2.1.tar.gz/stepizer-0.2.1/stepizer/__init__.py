__version__ = '0.2.1'

from stepizer.loader import (
    BatchLoader, FunctionLoader, GeneratorLoader, Loader, MultiprocessingLoader)
from stepizer.proxy import DefaultProxy, MultipleProxy, PersistentProxy, Proxy
from stepizer.register import Register, loaders, proxies
from stepizer.step import Step

__all__ = [
    'BatchLoader',
    'DefaultProxy',
    'FunctionLoader',
    'GeneratorLoader',
    'Loader',
    'MultipleProxy',
    'MultiprocessingLoader',
    'PersistentProxy',
    'Proxy',
    'Register',
    'Step',
    'loaders',
    'proxies',
]
