from dataclasses import dataclass
from explkttns.properties.player import PlayerProperty

class ExplosionImminent(PlayerProperty):
    pass

class NoDrawing(PlayerProperty):
    pass

@dataclass
class ExtraTurns(PlayerProperty):
    turns: int = 1

    def __post_init__(self):
        if self.turns < 0:
            raise ValueError("Number of turns cannot be negative.")
