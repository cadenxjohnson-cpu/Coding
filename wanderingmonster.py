from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class WanderingMonster:
    """
    A monster that wanders around on the grid map.

    This class is used for monsters shown on the pygame map.
    """
    name: str
    row: int       # y on the grid
    col: int       # x on the grid
    color: tuple   # (R, G, B)
    health: int
    power: int
    money: int

    def pos(self) -> tuple[int, int]:
        """Return (row, col) position on the grid."""
        return self.row, self.col

    def move_random(
        self,
        max_rows: int,
        max_cols: int,
        blocked_cells: set[tuple[int, int]],
    ) -> None:
        """
        Move one tile in a random legal direction (or stay if no legal moves).

        - Stays inside 0..max_rows-1 and 0..max_cols-1
        - Avoids any cell in blocked_cells (like the town square).
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for drow, dcol in directions:
            new_r = self.row + drow
            new_c = self.col + dcol

            if (
                0 <= new_r < max_rows
                and 0 <= new_c < max_cols
                and (new_r, new_c) not in blocked_cells
            ):
                self.row = new_r
                self.col = new_c
                break

    @classmethod
    def new_random_monster(
        cls,
        max_rows: int,
        max_cols: int,
        occupied_cells: set[tuple[int, int]],
        town_pos: tuple[int, int],
    ) -> "WanderingMonster":
        """
        Create a new random wandering monster.

        - Chooses a random monster type (name, color, stats).
        - Picks a random free tile that is:
            * inside the map,
            * not the town square,
            * not in occupied_cells.
        """
        monster_types = [
            # name       color           health power money
            ("Zombie",   (255, 0, 0),     25,   6,    20),
            ("Slime",    (0, 255, 0),     20,   4,    10),
            ("Ghost",    (200, 200, 255), 18,   5,    15),
        ]

        name, color, health, power, money = random.choice(monster_types)

        while True:
            r = random.randint(0, max_rows - 1)
            c = random.randint(0, max_cols - 1)
            if (r, c) != town_pos and (r, c) not in occupied_cells:
                break

        return cls(
            name=name,
            row=r,
            col=c,
            color=color,
            health=health,
            power=power,
            money=money,
        )
