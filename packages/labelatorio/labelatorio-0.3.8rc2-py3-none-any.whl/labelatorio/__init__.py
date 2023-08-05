from .client import Client
from .serving import *
from .query_model import DocumentQueryFilter


__version__=None
if __version__ is None:
    import os
    with open(os.path.join(os.path.dirname(__file__),"version.info"),"rt") as f:
        __version__= f.read()