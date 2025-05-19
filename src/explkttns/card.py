from dataclasses import dataclass
from typing import List, Set

from explkttns.properties.card import CardProperty
from explkttns.properties.card.base import Defuse, ExplodingKitten

@dataclass
class Card:
    name: str
    properties: List[CardProperty]
    description: str

def all_setup_cards() -> list[Card]:
    """
    Returns a list of all cards to be set up in the game.
    """
    return [PLACEHOLDER() for _ in range(56)] # W.I.P

# All cards
# (lambda prevents set mutability problems)
PLACEHOLDER = lambda: Card(".", [], "")
DEFUSE = lambda: Card("Defuse", [Defuse()], "")
EXPLODING_KITTEN = lambda: Card("Explosive Kitten", [ExplodingKitten()], "")
