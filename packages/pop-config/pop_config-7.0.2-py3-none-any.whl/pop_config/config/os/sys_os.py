"""
Read in keys - AKA Environement variables
"""
import os

__virtualname__ = "system"


def __virtual__(hub):
    """
    Load virtual
    """
    # future
    # if we need to add os specific stuff do it here
    return (True,)


def collect(hub, key):
    """
    Collect the option from environment variable if present
    """
    key = key.upper()
    if key in os.environ:
        return os.environ[key]
    return None
