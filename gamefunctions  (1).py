import random

# purchase_item function
def purchase_item(itemPrice: float, startingMoney: float, quantityToPurchase: int = 1):
    max_quantity = int(startingMoney // itemPrice)
    quantity_purchased = min(quantityToPurchase, max_quantity)
    remaining_money = startingMoney - (quantity_purchased * itemPrice)
    return quantity_purchased, remaining_money

# new_random_monster function
def new_random_monster():
    monster_names = ['Goblin', 'Giant Spider', 'Shrek']
    name = random.choice(monster_names)
    
    if name == 'Goblin':
        health = random.randint(10, 20)
        power = random.randint(5, 10)
        money = round(random.uniform(5, 15), 2)
        description = "In he distance you spot a lone goblin. It notices you and rushes at you quickly with a sword."
    elif name == 'Giant Spider':
        health = random.randint(100, 200)
        power = random.randint(30, 50)
        money = round(random.uniform(200, 1500), 2)
        description = "You are exploriung a giant cave and stumble across a giant spider, this spider has a giant web witht the remians of many advetures before you, you could be rich!"
    elif name == 'Shrek':
        health = random.randint(30, 50)
        power = random.randint(15, 25)
        money = round(random.uniform(10, 50), 2)
        description = "A huge ogre blocks your path and says you are in my swamp and a donkey comes out from behind him with a suit of donkey armor, they are ready to fight you"

    return {'name': name, 'description': description, 'health': health, 'power': power, 'money': money}

# game
def main():
    print("Welcome")
    player_money = 50.0  # starting money
    playing = True

    while playing:
        print("\nYou have ${:.2f}.".format(player_money))
        print("What would you like to do?")
        print("1. Purchase an item")
        print("2. Explore")
        print("3. Quit")

        choice = input("Enter your choice (1, 2, 3): ")

        if choice == '1':
            item_price = float(input("\nEnter  price item to purchase: "))
            quantity = int(input("Enter quantity to purchase: "))
            num_purchased, player_money = purchase_item(item_price, player_money, quantity)
            print(f"\nYou purchased {num_purchased} item(s). You have ${player_money:.2f} left.")

        elif choice == '2':
            print("\nYou are about to encounter a monster")
            monster = new_random_monster()
            print(f"\n A {monster['name']} appears!")
            print(f"Description: {monster['description']}")
            print(f"Health: {monster['health']}, Power: {monster['power']}, Money: ${monster['money']:.2f}")

            fight_choice = input("\nDo you want to fight the monster? (yes/no): ")
            if fight_choice == 'yes':
                print(f"\nYou fight with the {monster['name']}!")
                if random.random() > 0.5:  # 50 chance of winning
                    print(f"You defeated the {monster['name']} and gained ${monster['money']:.2f}!")
                    player_money += monster['money']
                else:
                    print(f"The {monster['name']} defeated you! you escaped.")
            else:
                print(f"\n you were scared a didnt fight {monster['name']} .")

        elif choice == '3':
            print("\n goodbye")
            playing = False

        else:
            print("\nInvalid choice. 1, 2, or 3.")

if __name__ == "__main__":
    main()
