from dataclasses import dataclass, field
from enum import IntEnum
from typing import List

@dataclass(frozen=True)
class Card:
    name: str = ""
    description: str = ""

@dataclass(frozen=True)
class ActionCard(Card):
    pass

@dataclass(frozen=True)
class ExplodingKitten(Card):
    name: str = "Exploding Kitten"
    description: str = "Explode and lose the game unless you have a defuse card."

@dataclass(frozen=True)
class Defuse(Card):
    name: str = "Defuse"
    description: str = "Defuse an exploding kitten."

@dataclass(frozen=True)
class Attack(ActionCard):
    name: str = "Attack"
    description: str = "End your turn without drawing a card and force the next player to take two turns."

@dataclass(frozen=True)
class Skip(ActionCard):
    name: str = "Skip"
    description: str = "End your turn without drawing a card."

@dataclass(frozen=True)
class Favor(ActionCard):
    name: str = "Favor"
    description: str = "Force another player to give you a card of their choice."

@dataclass(frozen=True)
class Shuffle(ActionCard):
    name: str = "Shuffle"
    description: str = "Shuffle the draw pile."

@dataclass(frozen=True)
class SeeTheFuture(ActionCard):
    name: str = "See the Future"
    description: str = "Look at the top three cards of the draw pile without revealing them."

@dataclass(frozen=True)
class Nope(ActionCard):
    name: str = "Nope"
    description: str = "Stop any action except for an exploding kitten or a defuse card."

@dataclass(frozen=True)
class CatCard(Card):
    name: str = "Cat Card"
    description: str = "Cat cards can be used to form pairs and steal cards from other players."

@dataclass(frozen=True)
class TacoCat(Card):
    name: str = "Taco Cat"

@dataclass(frozen=True)
class RainbowRalphingCat(Card):
    name: str = "Rainbow Ralphing Cat"

@dataclass(frozen=True)
class BeardCat(Card):
    name: str = "Beard Cat"

@dataclass(frozen=True)
class HairyPotatoCat(Card):
    name: str = "Hairy Potato Cat"

@dataclass(frozen=True)
class Cattermelon(Card):
    name: str = "Cattermelon"

def all_setup_cards() -> List[Card]:
    amount_each_card = {
        Attack: 4,
        Skip: 4,
        Favor: 4,
        Shuffle: 4,
        SeeTheFuture: 5,
        Nope: 5,
        TacoCat: 4,
        RainbowRalphingCat: 4,
        BeardCat: 4,
        HairyPotatoCat: 4,
        Cattermelon: 4,
    }
    cards = []
    for card_class, amount in amount_each_card.items():
        cards.extend([card_class()] * amount)
    return cards

class CardEnum(IntEnum):
    ATTACK = 0
    SKIP = 1
    FAVOR = 2
    SHUFFLE = 3
    SEE_THE_FUTURE = 4
    NOPE = 5
    EXPLODING_KITTEN = 6
    DEFUSE = 7
    TACO_CAT = 8
    RAINBOW_RALPHING_CAT = 9
    BEARD_CAT = 10
    HAIRY_POTATO_CAT = 11
    CATTERMELON = 12

card_enum_mapping: dict[CardEnum, type[Card]] = {
    CardEnum.ATTACK: Attack,
    CardEnum.SKIP: Skip,
    CardEnum.FAVOR: Favor,
    CardEnum.SHUFFLE: Shuffle,
    CardEnum.SEE_THE_FUTURE: SeeTheFuture,
    CardEnum.NOPE: Nope,
    CardEnum.EXPLODING_KITTEN: ExplodingKitten,
    CardEnum.DEFUSE: Defuse,
    CardEnum.TACO_CAT: TacoCat,
    CardEnum.RAINBOW_RALPHING_CAT: RainbowRalphingCat,
    CardEnum.BEARD_CAT: BeardCat,
    CardEnum.HAIRY_POTATO_CAT: HairyPotatoCat,
    CardEnum.CATTERMELON: Cattermelon
}
