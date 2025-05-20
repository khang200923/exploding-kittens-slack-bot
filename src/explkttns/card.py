from dataclasses import dataclass
from typing import List, Set

from explkttns.properties.card import CardProperty
from explkttns.properties.card.base import Attack, BeardCat, Cattermelon, Defuse, ExplodingKitten, Favor, HairyPotatoCat, Nope, RainbowRalphingCat, SeeTheFuture, Shuffle, Skip, TacoCat

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
ATTACK = lambda: Card("Attack", [Attack()], "")
SKIP = lambda: Card("Skip", [Skip()], "")
FAVOR = lambda: Card("Favor", [Favor()], "")
SHUFFLE = lambda: Card("Shuffle", [Shuffle()], "")
SEE_THE_FUTURE = lambda: Card("See the Future", [SeeTheFuture()], "")
NOPE = lambda: Card("Nope", [Nope()], "")
TACOCAT = lambda: Card("Taco Cat", [TacoCat()], "")
HAIRY_POTATOCAT = lambda: Card("Hairy Potato Cat", [HairyPotatoCat()], "")
BEARDCAT = lambda: Card("Beard Cat", [BeardCat()], "")
CATTEMELON = lambda: Card("Cattermelon", [Cattermelon()], "")
RAINBOW_RALPHING_CAT = lambda: Card("Rainbow Ralphing Cat", [RainbowRalphingCat()], "")
