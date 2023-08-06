"""
    Package to support the creation of valid bids-datasets.
"""
from .bidstaskevent import BIDSTaskEvent
from .bidstaskevent import BIDSError
from .bidshandler import BIDSHandler

__all__ = ["BIDSTaskEvent", "BIDSError", "BIDSHandler"]
