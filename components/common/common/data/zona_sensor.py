""" 
Enumeracion de zonas de sensores.
"""

from enum import Enum

class ZonaSensor(Enum):
    """ 
    Enumeracion con las zonas de los sensores
    """
    AMBIENTE = 1
    MACETA = 2
    SUELO = 3
    OTRA = 99