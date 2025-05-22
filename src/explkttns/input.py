from dataclasses import dataclass, field
from enum import Enum

class InputTypes(Enum):
    STOLEN_PLAYER = 0
    STOLEN_CARD_TYPE = 1
    STOLEN_CARD = 2
