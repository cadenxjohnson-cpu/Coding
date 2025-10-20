"""Adventure Game utility functions and test

This module provides functions for a text-based adventure
game. It includes a print welcome banner, display a shop
menu, purchase items given a budget, and generate a random monster
encounter.  Functions are designed to be imported and used by another
file (game.py).

Dependencies:
 Only Python standard library: random

Usage:
  Import this module in another script and call the functions.  To run
  the built-in demonstrations, execute this file directly.

Typical usage example:

  import gamefunctions as gf
  gf.print_welcome("Ada")
  gf.print_shop_menu("Sword", "Shield", "Potion")
  qty, money = gf.purchase_item(15.0, 42.0, quantity_to_purchase=3)
  monster = gf.random_monster()
"""

from __future__ import annotations

import random
from typing import Dict, List, Tuple


def print_welcome(name: str, width: int = 20) -> None:
    """Display a centered welcome message for the player.

    Args:
      name (str): The player's name to include in the greeting.
      width (int, optional): The total banner width. Defaults to 20.

    Returns:
      None
    """
    message = f"Hello, {name}!"
    print(f"{message:^{width}}")


def print_shop_menu(
    item1: str,
    item2: str,
    item3: str,
    prices: List[float] | None = None,
) -> None:
    """Print a shop menu listing three items and their prices.

    Args:
      item1 (str): The first item name.
      item2 (str): The second item name.
      item3 (str): The third item name.
      prices (list[float] | None, optional): The prices for the three
        items in order. If omitted, defaults to [25, 40, 15].

    Returns:
      None

    Example:
      >>> print_shop_menu("Sword", "Shield", "Potion", [25, 40, 15])
    """
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
    """Calculate how many items can be bought and the leftover money.

    Args:
      item_price (float): The cost of a single item.
      starting_money (float): The player's available money.
      quantity_to_purchase (int): The requested quantity to buy.

    Returns:
      tuple[int, float]: (quantity_purchased, remaining_money)

    Example:
      >>> purchase_item(15.0, 50.0, 3)
      (3, 5.0)
    """
    if item_price <= 0:
        return 0, starting_money
    max_quantity = int(starting_money // item_price)
    quantity_purchased = min(quantity_to_purchase, max_quantity)
    remaining_money = round(starting_money - (quantity_purchased * item_price), 2)
    return quantity_purchased, remaining_money


def random_monster() -> Dict[str, object]:
    """Generate a random monster encounter with stats and description.

    Returns:
      dict: A dictionary containing:
        - name (str): Monster type.
        - description (str): Flavored text for the encounter.
        - health (int): Monster hit points.
        - power (int): Monster attack power.
        - money (float): Gold dropped on victory.

    Example:
      >>> m = random_monster()
      >>> list(m.keys())
      ['name', 'description', 'health', 'power', 'money']
    """
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
    """Lightweight tests/demonstrations for this module.

    Runs if the module is executed directly.  Does not require any
    input from the user.
    """
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


if __name__ == "__main__":
    # When this file is run directly, exercise the functions.
    test_functions()

