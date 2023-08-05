from .client import Client
from .serving import *
from .query_model import DocumentQueryFilter


__version__=None
if __version__ is None:
    with open(__file__.replace("__init__.py","version.info"),"rt") as f:
        __version__=f.read()