"""Adventure Game utility functions and test

provides functions for a text-based adventure
game, print welcome banner, display a shop
menu, purchase items given a budget, and generate a random monster
encounter
file (game.py).



Dependencies:
  - Python standard library: json, random, typing
  - pygame
"""

from __future__ import annotations

import json
import random
from typing import Dict, List, Tuple

import pygame

from wanderingMonster import WanderingMonster

TILE_SIZE = 32
GRID_SIZE = 10
SCREEN_SIZE = GRID_SIZE * TILE_SIZE

DEFAULT_MAP_STATE = {
    "player_x": 0,
    "player_y": 0,
    "town_x": 0,
    "town_y": 0,
    # runtime: list[WanderingMonster]; will be serialized for saves
    "monsters": [],
    "left_town": False,
    "player_move_count": 0,
    # index of monster tile we last collided with (for combat resolution)
    "last_monster_index": None,
}


def serialize_monsters(monsters: List[WanderingMonster]) -> List[dict]:
    """Convert WanderingMonster objects into plain dicts for JSON save."""
    data: List[dict] = []
    for m in monsters:
        data.append(
            {
                "name": m.name,
                "row": m.row,
                "col": m.col,
                "color": list(m.color),
                "health": m.health,
                "power": m.power,
                "money": m.money,
            }
        )
    return data


def deserialize_monsters(raw_list: List[dict]) -> List[WanderingMonster]:
    """Convert dicts loaded from JSON back into WanderingMonster objects."""
    monsters: List[WanderingMonster] = []
    for d in raw_list:
        monsters.append(
            WanderingMonster(
                name=d["name"],
                row=d["row"],
                col=d["col"],
                color=tuple(d["color"]),
                health=d["health"],
                power=d["power"],
                money=d["money"],
            )
        )
    return monsters


def ensure_two_monsters(map_state: dict) -> None:
    """
    Make sure there are at least two wandering monsters on the map.

    Called when the player enters the map and when all monsters
    have been defeated.
    """
    monsters: List[WanderingMonster] = map_state.get("monsters")
    if monsters is None or not isinstance(monsters, list):
        monsters = []
        map_state["monsters"] = monsters

    # if this came from a JSON load and still holds dicts, convert them
    if monsters and isinstance(monsters[0], dict):
        monsters = deserialize_monsters(monsters)
        map_state["monsters"] = monsters

    # Already have 2 or more
    if len(monsters) >= 2:
        return

    px = map_state.get("player_x", 0)
    py = map_state.get("player_y", 0)
    tx = map_state.get("town_x", 0)
    ty = map_state.get("town_y", 0)

    town_pos = (ty, tx)  # (row, col)
    occupied = {(py, px), town_pos}
    for m in monsters:
        occupied.add(m.pos())

    while len(monsters) < 2:
        new_m = WanderingMonster.new_random_monster(
            max_rows=GRID_SIZE,
            max_cols=GRID_SIZE,
            occupied_cells=occupied,
            town_pos=town_pos,
        )
        monsters.append(new_m)
        occupied.add(new_m.pos())


def move_monsters(map_state: dict) -> None:
    """Move all monsters one step (randomly), avoiding town and each other."""
    monsters: List[WanderingMonster] = map_state.get("monsters", [])
    tx = map_state.get("town_x", 0)
    ty = map_state.get("town_y", 0)
    town_pos = (ty, tx)

    for m in monsters:
        # other monsters + town are blocked
        blocked = {town_pos}
        for other in monsters:
            if other is not m:
                blocked.add(other.pos())

        # temporarily remove current position from blocked to allow moving out
        blocked.discard(m.pos())

        m.move_random(
            max_rows=GRID_SIZE,
            max_cols=GRID_SIZE,
            blocked_cells=blocked,
        )


def run_map(map_state: dict):
    """
    Pygame map loop.

    Returns:
      - ("quit_no_save", map_state) if window closed.
      - ("town", map_state) if the player returns to the town tile.
      - ("monster", map_state) if the player steps on a monster tile.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Adventure Map")
    clock = pygame.time.Clock()

    # unpack state
    px = map_state.get("player_x", 0)
    py = map_state.get("player_y", 0)
    tx = map_state.get("town_x", 0)
    ty = map_state.get("town_y", 0)
    left = map_state.get("left_town", False)
    player_move_count = map_state.get("player_move_count", 0)

    # ensure monsters list exists & has two monsters
    ensure_two_monsters(map_state)
    monsters: List[WanderingMonster] = map_state["monsters"]

    running = True
    result = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit_no_save", map_state

            if event.type == pygame.KEYDOWN:
                dx = dy = 0
                if event.key == pygame.K_UP:
                    dy = -1
                elif event.key == pygame.K_DOWN:
                    dy = 1
                elif event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1

                nx = px + dx
                ny = py + dy

                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    px, py = nx, ny
                    map_state["player_x"] = px
                    map_state["player_y"] = py

                    # mark that we left town once we step off the town tile
                    if not left and (px != tx or py != ty):
                        left = True
                        map_state["left_town"] = True

                    # every time the player actually moves, increment counter
                    player_move_count += 1
                    map_state["player_move_count"] = player_move_count

                    # move monsters every other time the player moves
                    if player_move_count % 2 == 0:
                        move_monsters(map_state)

                    # returning to town after leaving
                    if px == tx and py == ty and left:
                        result = "town"
                        running = False
                        break

                    # collision with any monster triggers combat
                    for idx, m in enumerate(monsters):
                        if px == m.col and py == m.row:
                            map_state["last_monster_index"] = idx
                            result = "monster"
                            running = False
                            break

        # draw scene
        screen.fill((0, 0, 0))

        # grid lines
        for gx in range(GRID_SIZE):
            for gy in range(GRID_SIZE):
                pygame.draw.rect(
                    screen,
                    (60, 60, 60),
                    (gx * TILE_SIZE, gy * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    1,
                )

        # town (green circle)
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (tx * TILE_SIZE + TILE_SIZE // 2, ty * TILE_SIZE + TILE_SIZE // 2),
            TILE_SIZE // 2 - 4,
        )

        # wandering monsters (colored circles by type)
        for m in monsters:
            pygame.draw.circle(
                screen,
                m.color,
                (m.col * TILE_SIZE + TILE_SIZE // 2, m.row * TILE_SIZE + TILE_SIZE // 2),
                TILE_SIZE // 2 - 4,
            )

        # player (blue square)
        pygame.draw.rect(
            screen,
            (0, 0, 255),
            (px * TILE_SIZE, py * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return result, map_state


def print_welcome(name: str, width: int = 20) -> None:
    """Display a centered welcome message for the player."""
    message = f"Hello, {name}!"
    print(f"{message:^{width}}")


def print_shop_menu(
    item1: str,
    item2: str,
    item3: str,
    prices: List[float] | None = None,
) -> None:
    """Print a shop menu listing three items and their prices."""
    if prices is None:
        prices = [25.0, 40.0, 15.0]
    print("\nWelcome to the shop! Here are your options:")
    print(f"1. {item1} - {prices[0]} gold coins")
    print(f"2. {item2} - {prices[1]} gold coins")
    print(f"3. {item3} - {prices[2]} gold coins")
    print()


def purchase_item(
    item_price: float,
    starting_money: float,
    quantity_to_purchase: int = 1,
) -> Tuple[int, float]:
    """Calculate how many items can be bought and the leftover money."""
    if item_price <= 0:
        return 0, starting_money
    max_quantity = int(starting_money // item_price)
    quantity_purchased = min(quantity_to_purchase, max_quantity)
    remaining_money = round(starting_money - (quantity_purchased * item_price), 2)
    return quantity_purchased, remaining_money


def random_monster() -> Dict[str, object]:
    """Generate a random monster encounter with stats and description."""
    monster_names = ["Goblin", "Giant Spider", "Ogre"]
    name = random.choice(monster_names)

    if name == "Goblin":
        health = random.randint(10, 20)
        power = random.randint(5, 10)
        money = round(random.uniform(5, 15), 2)
        description = (
            "In the distance you spot a lone goblin. It notices you and "
            "rushes at you with a sword."
        )
    elif name == "Giant Spider":
        health = random.randint(30, 50)
        power = random.randint(8, 15)
        money = round(random.uniform(10, 40), 2)
        description = (
            "You stumble across a giant spider guarding a web filled with "
            "shiny trinkets."
        )
    else:  # Ogre
        health = random.randint(25, 40)
        power = random.randint(10, 18)
        money = round(random.uniform(8, 30), 2)
        description = (
            "A hulking ogre blocks your path and bellows, 'Turn back!'"
        )

    return {
        "name": name,
        "description": description,
        "health": health,
        "power": power,
        "money": money,
    }


def test_functions() -> None:
    """Lightweight tests/demonstrations for this module."""
    print("== test: print_welcome ==")
    print_welcome("Tester", width=24)

    print("\n== test: print_shop_menu ==")
    print_shop_menu("Sword", "Shield", "Potion")

    print("\n== test: purchase_item ==")
    bought, left = purchase_item(15.0, 50.0, 3)
    print(f"Purchased: {bought}, Remaining: ${left:.2f}")

    print("\n== test: random_monster ==")
    m = random_monster()
    print(f"Encountered: {m['name']} (HP {m['health']}, PWR {m['power']})")
    print(f"Loot: ${m['money']:.2f}")
    print(m['description'])


def save_game(filename, name, hp, gold, inventory, map_state):
    # Make a shallow copy so we don't mutate the runtime map_state
    map_state_copy = dict(map_state)

    # Serialize monsters if needed
    monsters = map_state_copy.get("monsters", [])
    if monsters and isinstance(monsters[0], WanderingMonster):
        map_state_copy["monsters"] = serialize_monsters(monsters)

    data = {
        "name": name,
        "hp": hp,
        "gold": gold,
        "inventory": inventory,
        "map_state": map_state_copy,
    }
    with open(filename, "w") as f:
        json.dump(data, f)


def load_game(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        map_state = data.get("map_state", DEFAULT_MAP_STATE.copy())

        # Backwards compatibility: if old keys exist but no monsters list,
        # start with an empty monster list (we'll spawn when entering map).
        if "monsters" not in map_state:
            map_state["monsters"] = []

        # Ensure left_town and counters exist
        map_state.setdefault("left_town", False)
        map_state.setdefault("player_move_count", 0)
        map_state.setdefault("last_monster_index", None)

        # If monsters are stored as dicts, convert back to objects
        monsters = map_state.get("monsters", [])
        if monsters and isinstance(monsters[0], dict):
            map_state["monsters"] = deserialize_monsters(monsters)

        data["map_state"] = map_state
        return data
    except FileNotFoundError:
        print("Save not found, starting new game.")
        return {
            "name": "Adventurer",
            "hp": 30,
            "gold": 10,
            "inventory": [],
            "map_state": DEFAULT_MAP_STATE.copy(),
        }


if __name__ == "__main__":
    test_functions()
