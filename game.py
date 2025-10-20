"""Basic funtions that supports imports gamefunctions

Prompts for the player's name, shows the shop, offers a simple purchase,
and rolls a random monster encounter.
"""

from __future__ import annotations

import gamefunctions as gf


def main() -> None:
    name = input("Enter your name: ").strip() or "Adventurer"
    gf.print_welcome(name)

    # Show shop menu
    items = ("Sword", "Shield", "Potion")
    prices = [25.0, 40.0, 15.0]
    gf.print_shop_menu(*items, prices=prices)

    # Simple purchase flow
    try:
        choice = int(input("Pick an item (1-3): "))
        if choice not in (1, 2, 3):
            raise ValueError
        price = prices[choice - 1]
        qty = int(input("Quantity to buy: "))
        bought, remaining = gf.purchase_item(price, starting_money=50.0, quantity_to_purchase=qty)
        print(f"You bought {bought} item(s). You have ${remaining:.2f} left.")
    except ValueError:
        print(" Skipping purchase")

    # Random encounter
    print("\nYou venture forth...")
    monster = gf.random_monster()
    print(f"A wild {monster['name']} appears!")
    print(f"HP {monster['health']}  PWR {monster['power']}  Loot ${monster['money']:.2f}")
    print(monster["description"])


if __name__ == "__main__":
    main()

