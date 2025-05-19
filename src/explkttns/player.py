from dataclasses import dataclass, field
from typing import List, Set

from explkttns.card import Card
from explkttns.properties.player import PlayerProperty

@dataclass
class Player:
    name: str
    hand: List[Card]
    properties: List[PlayerProperty]
