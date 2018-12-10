# -*- coding: utf-8 -*-
"""UPNP device mapping tool"""


import logging
from logging import NullHandler

logger = logging.getLogger('UPNP_Devices')
logger.addHandler(NullHandler())
logging.basicConfig(format="%(message)s", level=None)

logger.setLevel(logging.NOTSET)


from .discover import discover # NOQA
from .listen import listen # NOQA


__title__ = "UPNP_Device"
__version__ = "0.1.1b"
__url__ = "https://github.com/kdschlosser/UPNP_Device"
__author__ = "Kevin Schlosser"
__author_email__ = "kevin.g.schlosser@gmail.com"
__license__ = open('LICENSE').read()
__all__ = (
    '__title__', '__version__', '__url__', '__author__', '__author_email__',
    '__license__', 'discover'
)

