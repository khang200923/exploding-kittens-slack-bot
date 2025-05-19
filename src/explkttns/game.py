"""
Exploding Kittens card game!
"""
from dataclasses import dataclass, field
import random
from typing import List

from explkttns.card import DEFUSE, EXPLODING_KITTEN, Card, all_setup_cards
from explkttns.player import Player

@dataclass
class Game:
    names: List[str]
    players: List[Player] = field(init=False)
    deck: List[Card] = field(init=False)
    current_player: int = field(init=False)

    def __post_init__(self):
        self.players = []
        deck = all_setup_cards()
        for name in self.names:
            hand = random.sample(self.deck, k=4)
            deck = [card for card in deck if card not in hand]
            hand.append(DEFUSE())
            player = Player(name, hand, [])
            self.players.append(player)
        deck.extend([EXPLODING_KITTEN()] * (len(self.players) - 1))
        self.deck = deck
        self.current_player = random.randrange(len(self.players))
