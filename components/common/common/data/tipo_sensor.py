""" Sentiments enumeration module.
"""

from enum import Enum

class TipoSensor(Enum):
    """ Enumeration with the sentiments.
    """
    HUMEDAD_AMBIENTE = 1
    HUMEDAD_SUELO = 2
    TEMPERATURA = 3
    LUZ = 4
