""" Role enumeration module.
"""

from enum import Enum

class Role(Enum):
    """ Enumeration with the roles.
    """
    ADMINISTRATION = 1
    MODERATION = 2
    DISCUSSION = 3
