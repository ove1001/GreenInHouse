""" 
Enumeracion de tipos de sensores.
"""

from enum import Enum

class TipoSensor(Enum):
    """ 
    Enumeracion con los tipos de sensores
    """
    HUMEDAD = 1
    TEMPERATURA = 2
    LUZ = 3
    OTRO = 99