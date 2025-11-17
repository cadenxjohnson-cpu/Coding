"""
text based adventure game that uses functions from gamefunctions.py
"""

from __future__ import annotations
import random
import gamefunctions as gf


def fight_monster(name, hp, gold, inventory):
    """Monster fight loop."""
    monster = gf.random_monster()
    print(f"\nA wild {monster['name']} appears (HP {monster['health']}, Power {monster['power']})")

    while hp > 0 and monster["health"] > 0:
        print(f"\n{name}'s HP: {hp} | {monster['name']}'s HP: {monster['health']}")
        print("1) Attack  2) Run")
        action = input("Choose: ").strip()

        if action == "1":
            player_hit = random.randint(5, 10)
            monster_hit = random.randint(2, monster["power"])
            monster["health"] -= player_hit
            hp -= monster_hit
            print(f"You hit for {player_hit}. The monster hits back for {monster_hit}.")
        elif action == "2":
            print("You ran away")
            break
        else:
            print("Error.")

    if hp <= 0:
        print("You fainted, You wake up back in town with 10 HP.")
        hp = 10
    elif monster["health"] <= 0:
        print(f"You defeated the {monster['name']} and earned {monster['money']} gold.")
        gold += monster["money"]

        # Chance to get an item drop
        if random.random() < 0.5:
            item = {"name": "Sword", "type": "weapon", "maxDurability": 10, "currentDurability": 10}
            inventory.append(item)
            print(f"You found a {item['name']}")

    return hp, gold, inventory


def view_inventory(inventory):
    """Display all items in inventory"""
    if not inventory:
        print("\nYour inventory is empty")
        return
    print("\n--- Inventory ---")
    for i, item in enumerate(inventory, 1):
        info = ", ".join([f"{k}: {v}" for k, v in item.items()])
        print(f"{i}) {info}")


def main():
    """Main game loop."""
    print("Welcome to the Adventure Game!")
    print("1) Start New Game")
    print("2) Load Saved Game")
    start_choice = input("Choose: ").strip()

    if start_choice == "2":
        filename = input("Enter filename to load (e.g., save1.json): ").strip()
        data = gf.load_game(filename)
        name = data.get("name", "Adventurer")
        hp = data.get("hp", 30)
        gold = data.get("gold", 10)
        inventory = data.get("inventory", [])
        map_state = data.get("map_state", gf.DEFAULT_MAP_STATE.copy())
    else:
        name = input("Enter your name: ").strip() or "Adventurer"
        gf.print_welcome(name)
        hp = 30
        gold = 10
        inventory = []
        map_state = gf.DEFAULT_MAP_STATE.copy()

    while True:
        print(f"\nYou are in town.\nCurrent HP: {hp}, Gold: {gold}")
        print("1) Leave town (Explore Map)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) View Inventory")
        print("4) Save and Quit")

        choice = input("Choose: ").strip()

        # --- MAP OPTION ---
        if choice == "1":
            action, map_state = gf.run_map(map_state)

            if action == "quit_no_save":
                print("Game closed without saving.")
                return

            if action == "monster":
                hp, gold, inventory = fight_monster(name, hp, gold, inventory)

                if hp <= 0:
                    print("You died. Game Over.")
                    break

                # After the fight, return to the same tile
                action, map_state = gf.run_map(map_state)
                if action == "quit_no_save":
                    print("Game closed without saving.")
                    return

        elif choice == "2":
            if gold >= 5:
                gold -= 5
                hp = 30
                print("You rest and feel refreshed. HP fully restored!")
            else:
                print("Not enough gold to rest.")

        elif choice == "3":
            view_inventory(inventory)

        elif choice == "4":
            filename = input("Enter filename to save (e.g., save1.json): ").strip()
            gf.save_game(filename, name, hp, gold, inventory, map_state)
            print("Game saved! Goodbye.")
            break

        else:
            print("Error, try again.")


if __name__ == "__main__":
    main()
