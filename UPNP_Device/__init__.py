


import logging
from logging import NullHandler

logger = logging.getLogger('UPNP_Devices')
logger.addHandler(NullHandler())
logging.basicConfig(format="%(message)s", level=None)

logger.setLevel(logging.NOTSET)


from .discover import discover
from .listen import listen
