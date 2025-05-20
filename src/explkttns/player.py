from dataclasses import dataclass, field
from typing import List, Set

from explkttns.card import Card

@dataclass
class Player:
    name: str
    hand: List[Card] = field(default_factory=list)
    dead: bool = False
