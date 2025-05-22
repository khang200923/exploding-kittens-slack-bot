from dataclasses import dataclass, field
from typing import Callable, List, Set

from explkttns.card import Card

@dataclass
class Player:
    name: str
    hand: List[Card] = field(default_factory=list)
    future_callback: Callable[[List[Card]], None] = field(default=lambda x: None)
    dead: bool = False
