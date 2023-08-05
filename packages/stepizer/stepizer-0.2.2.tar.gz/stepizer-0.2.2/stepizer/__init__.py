__version__ = '0.2.2'

from stepizer.loader import (
    BatchLoader, FunctionLoader, GeneratorLoader, Loader, MultiprocessingLoader)
from stepizer.proxy import DefaultProxy, MultiOutputProxy, Proxy, SingleOutputProxy
from stepizer.register import Register, loaders, proxies
from stepizer.step import Step

__all__ = [
    'BatchLoader',
    'DefaultProxy',
    'FunctionLoader',
    'GeneratorLoader',
    'Loader',
    'MultiOutputProxy',
    'MultiprocessingLoader',
    'Proxy',
    'Register',
    'SingleOutputProxy',
    'Step',
    'loaders',
    'proxies',
]
