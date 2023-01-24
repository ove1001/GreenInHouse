""" Report statuses enumeration module.
"""

from enum import Enum

class ReportStatus(Enum):
    """ Enumeration with the report statuses.
    """
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3
