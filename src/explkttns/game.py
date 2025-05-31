from dataclasses import dataclass, field
import random
from typing import List

from src.explkttns.card import Attack, Card, CardEnum, Defuse, ExplodingKitten, Favor, Nope, SeeTheFuture, Shuffle, Skip, all_setup_cards, card_enum_mapping
from src.explkttns.input import InputTypes
from src.explkttns.player import Player

class IllegalMoveError(Exception):
    pass

@dataclass
class Game:
    names: List[str]
    players: List[Player] = field(init=False)
    deck: List[Card] = field(init=False)
    current_player: int = field(init=False)

    ready_cards: List[Card] = field(init=False)
    nope_effect: bool = field(default=False)
    incoming_input: int = field(default=0)

    # important note: turns_required becomes the number of additional
    # turns delegated to the second player while Attack cards stack
    turns_required: int = field(default=1)
    attacks_stack: int = field(default=0)

    must_draw: bool = field(default=True)

    def __post_init__(self):
        self.players = []
        self.ready_cards = []
        self.deck = all_setup_cards()
        for name in self.names:
            hand = random.sample(self.deck, k=4)
            self.deck = [card for card in self.deck if card not in hand]
            hand.append(Defuse())
            player = Player(name, hand=hand)
            self.players.append(player)
        self.current_player = random.randrange(len(self.players))
        self.deck.extend([ExplodingKitten()] * (len(self.players) - 1))
        random.shuffle(self.deck)

    def play(self, playing_player: int, cards: List[int]):
        player = self.players[playing_player]
        if player.dead:
            raise ValueError("Player is dead and cannot play cards.")
        for card in sorted(cards, reverse=True):
            if card < 0 or card >= len(player.hand):
                raise ValueError("Invalid card index")
            played_card = player.hand.pop(card)
            if isinstance(played_card, Nope):
                self.nope_effect = not self.nope_effect
                return
            self.ready_cards.append(played_card)
        if self.turns_required > 0:
            self.turns_required -= 1

    def draw(self):
        player = self.players[self.current_player]
        assert not player.dead, "Wait something's wrong"
        assert self.must_draw, "..."
        assert self.deck, "This is logically impossible"
        drawn_card = self.deck.pop(0)
        if isinstance(drawn_card, ExplodingKitten):
            # shoot use the defuse card QUICK
            if any(isinstance(card, Defuse) for card in player.hand):
                player.hand.remove(next(card for card in player.hand if isinstance(card, Defuse)))
                yield (self.current_player, InputTypes.WHERE_TO_INSERT_EXPLODING_KITTEN_CARD)
                self.deck.insert(self.incoming_input, drawn_card)
                return
            # you're dead lol
            player.dead = True
            return
        player.hand.append(drawn_card)


    def next_player(self, current_player: int) -> int:
        next_player = (current_player + 1) % len(self.players)
        while self.players[next_player].dead:
            next_player = (next_player + 1) % len(self.players)
        return next_player

    def end_turn(self):
        if self.turns_required > 0 and self.attacks_stack:
            raise IllegalMoveError("Must fulfill required turns or play an Attack card")
        if self.must_draw:
            gen = self.draw()
            try:
                while True:
                    request = next(gen)
                    yield request
            except StopIteration:
                pass

        self.switch_player()

    def switch_player(self):
        self.current_player = self.next_player(self.current_player)
        self.must_draw = True
        if self.attacks_stack:
            self.turns_required += 2 * self.attacks_stack
            self.attacks_stack = 0
        else:
            self.turns_required = 1

    def take_effect(self, playing_player: int):
        ready_cards = self.ready_cards.copy()
        self.ready_cards.clear()
        player = self.players[playing_player]
        if self.nope_effect:
            self.nope_effect = False
            return
        if len(ready_cards) == 0:
            return
        if len(ready_cards) == 2:
            if ready_cards[0].name != ready_cards[1].name:
                raise IllegalMoveError("Cannot play two different cards as a special combo.")
            yield InputTypes.STOLEN_PLAYER
            stolen_player = self.players[self.incoming_input]
            if not stolen_player.hand:
                return # lmao
            stolen_card = stolen_player.hand.pop(random.randrange(len(stolen_player.hand)))
            player.hand.append(stolen_card)
            return
        if len(ready_cards) == 3:
            if ready_cards[0].name != ready_cards[1].name:
                raise IllegalMoveError("Cannot play three different cards as a special combo.")
            if ready_cards[0].name != ready_cards[2].name:
                raise IllegalMoveError("Cannot play three different cards as a special combo.")
            yield (playing_player, InputTypes.STOLEN_PLAYER)
            stolen_player = self.players[self.incoming_input]
            yield (playing_player, InputTypes.STOLEN_CARD_TYPE)
            stolen_card_type = card_enum_mapping[CardEnum(self.incoming_input)]
            if not any(card.name == stolen_card_type.name for card in stolen_player.hand):
                return
            stolen_card = next((card for card in stolen_player.hand if card.name == stolen_card_type.name), None)
            assert stolen_card is not None, "Card should be in hand"
            stolen_player.hand.remove(stolen_card)
            player.hand.append(stolen_card)

        ready_card = ready_cards[0]

        if isinstance(ready_card, Attack):
            self.attacks_stack += 1
            return
        if isinstance(ready_card, Skip):
            self.must_draw = False
            return
        if isinstance(ready_card, Favor):
            yield (playing_player, InputTypes.STOLEN_PLAYER)
            stolen_player = self.players[self.incoming_input]
            yield (self.incoming_input, InputTypes.STOLEN_CARD)
            stolen_card = stolen_player.hand.pop(self.incoming_input)
            player.hand.append(stolen_card)
            return
        if isinstance(ready_card, Shuffle):
            random.shuffle(self.deck)
            return
        if isinstance(ready_card, SeeTheFuture):
            future_cards = self.deck[:3] # colon three
            player.future_callback(future_cards)
            return
        assert not isinstance(ready_card, Nope), "Nope card should not be here..."

        # cat cards alone don't have any effect
        return
