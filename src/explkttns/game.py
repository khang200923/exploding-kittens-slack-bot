"""
Exploding Kittens card game!
"""
from dataclasses import dataclass, field
import random
from typing import List

from explkttns.card import DEFUSE, EXPLODING_KITTEN, Card, all_setup_cards
from explkttns.player import Player
from explkttns.properties.card.base import Attack, Defuse, ExplodingKitten, Favor, Skip
from explkttns.properties.player.base import ExplosionImminent, ExtraTurns, NoDrawing

class IllegalMoveError(Exception):
    pass

@dataclass
class Game:
    names: List[str]
    players: List[Player] = field(init=False)
    deck: List[Card] = field(init=False)
    current_player: int = field(init=False)
    card_queue: List[Card] = field(init=False) # Stores a card in case Nope interrupts it

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
        self.card_queue = []

    def next_player_index(self, current_player: int | None = None) -> int:
        """
        Returns the next player in the game.
        """
        if current_player is None:
            current_player = self.current_player
        return (current_player + 1) % len(self.players)

    def move_to_next_player(self):
        """
        Moves to the next player in the game.
        """
        self.current_player = self.next_player_index(self.current_player)
        return self.players[self.current_player]

    def play(self, current_player: int, indexes: List[int]):
        """
        Plays a card from the current player's hand.
        """
        player = self.players[current_player]
        for index in indexes:
            if index < 0 or index >= len(player.hand):
                raise IllegalMoveError("Invalid card index.")
            card = player.hand[index]
            player.hand.remove(card)
            self.card_queue.append(card)

    def take_effect(self, current_player: int, cards: List[Card] | None = None):
        """
        Takes effect of a card.
        """
        if cards is None:
            if not self.card_queue:
                raise IllegalMoveError("No card to take effect.")
            cards = self.card_queue
            self.card_queue = []
        player = self.players[current_player]
        if len(cards) > 1:
            assert False, "W.I.P."
        card = cards[0]
        assert not isinstance(card, ExplodingKitten)
        if isinstance(card, Defuse):
            if ExplosionImminent() not in player.properties:
                raise IllegalMoveError("No Exploding Kitten in play.")
            player.properties.remove(ExplosionImminent())
        if isinstance(card, Attack):
            self.players[current_player].properties.append(NoDrawing())
            self.players[self.next_player_index()].properties.append(ExtraTurns(2))
        if isinstance(card, Skip):
            self.players[current_player].properties.append(NoDrawing())
        # W.I.P
