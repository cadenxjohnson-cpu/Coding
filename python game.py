""" text based game that uses functions from gamefunctions.py

Asks the player's name, displays a simple shop, allows fighting
monsters, sleeping to restore HP, and quitting the game.
"""

from __future__ import annotations
import random
import gamefunctions as gf


def fight_monster(name, hp, gold):
    """ monster fight loop."""
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
            print(f"You hit for {player_hit} The monster hits back for {monster_hit}")
        elif action == "2":
            print("You ran away!")
            break
        else:
            print("Error")

    if hp <= 0:
        print("You fainted, You wake up back in town with 10 HP")
        hp = 10
    elif monster["health"] <= 0:
        print(f"You defeated the {monster['name']} and earned {monster['money']} gold")
        gold += monster["money"]

    return hp, gold


def main():
    """Main game loop."""
    name = input("Enter your name: ").strip() or "Adventurer"
    gf.print_welcome(name)

    hp = 30
    gold = 10

    while True:
        print(f"\nYou are in town.\nCurrent HP: {hp}, Gold: {gold}")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Quit")

        choice = input("Choose: ").strip()

        if choice == "1":
            hp, gold = fight_monster(name, hp, gold)
        elif choice == "2":
            if gold >= 5:
                gold -= 5
                hp = 30
                print("You rest and feel refreshed HP fully restored")
            else:
                print("Not enough gold to rest")
        elif choice == "3":
            print("Bye")
            break
        else:
            print("Error try again.")


if __name__ == "__main__":
    main()
