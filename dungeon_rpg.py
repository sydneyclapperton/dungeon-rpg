#packages
import random
import time

"""#Object Creation

##Character
"""

#Player_Class Creation
CLASS_DATA = {
  "Warrior" : {"hp": 20,
                "min_damage":2,
                "max_damage":4,
                "potions":0,
                "ability": "Power Strike",
                "cooldown": 4,
                "ability_desc": "Doubles attack damage",
                "ability_effect": lambda x : x * 2},
  "Mage" : {"hp": -10,
              "min_damage":3,
              "max_damage":5,
              "potions":3,
              "ability": "Fireball",
              "cooldown": 3,
              "ability_desc": "Adds 15 damage to attack",
              "ability_effect": lambda x : x + 15},
  "Rogue" : {"hp": 0,
              "min_damage":0,
              "max_damage":7,
              "potions":1,
              "ability": "Knife Throw",
              "cooldown": 3,
              "ability_desc": "Doubles attack damage and adds 5",
              "ability_effect": lambda x : x*2 + 5},
  "Paladin" : {"hp": 30,
            "min_damage":1,
            "max_damage":2,
            "potions":2,
            "ability": "Smite",
            "cooldown": 2,
            "ability_desc": "Adds 10 damage to attack",
            "ability_effect": lambda x : x + 10}
}

#Object Creation
#Character
class Character:
  def __init__(self,name,player_class):
    self.name = name
    self.player_class = player_class
    self.level = 1
    self.xp = 0
    self.max_hp = 50
    self.hp = self.max_hp
    self.min_damage = 1
    self.max_damage = 10
    self.healing_potions = 1
    self.inventory = []
    self.equipment = {
      "Weapon": None,
      "Helmet": None,
      "Chest": None,
      "Boots": None
      }
    self.gold = 0
    class_bonus = CLASS_DATA.get(player_class, {})
    self.max_hp += class_bonus.get("hp", 0)
    self.min_damage += class_bonus.get("min_damage", 0)
    self.max_damage += class_bonus.get("max_damage", 0)
    self.healing_potions += class_bonus.get("potions", 0)
    self.hp = self.max_hp
    self.special_ability = class_bonus.get("ability")
    self.ability_effect = class_bonus.get("ability_effect")
    self.ability_desc = class_bonus.get("ability_desc")
    self.ability_cooldown = class_bonus.get("cooldown", 0)
    self.special_cooldown = 0

  def attack(self):
    return random.randint(self.min_damage, self.max_damage)

  def equip(self, item):
    old_item = self.equipment[item.slot]
    if old_item:
      self.max_hp -= old_item.hp_bonus
      self.min_damage -= old_item.min_dmg_bonus
      self.max_damage -= old_item.max_dmg_bonus
    self.equipment[item.slot] = item
    self.max_hp += item.hp_bonus
    self.min_damage += item.min_dmg_bonus
    self.max_damage += item.max_dmg_bonus
    self.hp = min(self.hp, self.max_hp)
    print(f"{self.name} equipped {item.name}!")

  def view_inventory(self):
    print(f"You have {self.healing_potions} potions and {self.gold} gold.")
    if not self.inventory:
      print("Inventory is empty.")
      return
    print("Inventory:")
    for i, item in enumerate(self.inventory, start=1):
      print(
          f"{i}. {item.name} | "
          f"HP +{item.hp_bonus} | "
          f"Min DMG +{item.min_dmg_bonus} | "
          f"Max DMG +{item.max_dmg_bonus} | "
          f"Value: {item.value}g")

  def level_up(self):
    xp_needed = self.level*5 - 2
    if self.xp >= xp_needed:
      self.level += 1
      self.min_damage += 2
      self.max_damage += 3
      self.max_hp += 10
      self.hp = self.max_hp
      self.xp -= xp_needed
      return True
    else:
      return False

  def view_equipped(self):
    print("Equipment: \n")
    for slot, item in self.equipment.items():
      if item:
        print(f"{slot}: {item.name} | "
        f"HP +{item.hp_bonus} | "
        f"Min DMG +{item.min_dmg_bonus} | "
        f"Max DMG +{item.max_dmg_bonus}")
      else:
        print(f"{slot}: None")

  def view_stats(self):
    return (f"Name: {self.name}\nClass: {self.player_class}\n"
          f"Ability: {self.special_ability}\nLevel: {self.level}\n"
          f"Effect: {self.ability_desc}\n"
          f"Current XP: {self.xp}/{self.level*5 - 2}\n\n"
          f"HP: {self.hp}/{self.max_hp}\n"
          f"Damage: {self.min_damage}-{self.max_damage}\n\n"
          f"Gold: {self.gold}\n"
          f"Potions: {self.healing_potions}")

  def equip_from_inventory(self):
    if not self.inventory:
        print("Your inventory is empty.")
        return
    print("Inventory:")
    for i, item in enumerate(self.inventory, start=1):
        print(
            f"{i}. {item.name} | "
            f"HP +{item.hp_bonus} | "
            f"Min DMG +{item.min_dmg_bonus} | "
            f"Max DMG +{item.max_dmg_bonus}")

    while True:
        try:
            choice = int(input("\nSelect an item to equip (0 to cancel): "))
            if choice == 0:
                return

            if 1 <= choice <= len(self.inventory):
                item = self.inventory[choice - 1]
                old_item = self.equipment[item.slot]
                self.equip(item)
                if old_item:
                  self.inventory.append(old_item)
                self.inventory.pop(choice - 1)
                print(f"{item.name} was removed from your inventory.")
                return
            print("Please select a valid item.")
        except ValueError:
            print("Please enter a number.")

  def sell_item(self):
      if not self.inventory:
          print("You have nothing to sell.")
          return
      print("Inventory:")
      for i, item in enumerate(self.inventory, start=1):
          value = getattr(item, "value", 5)
          print(f"{i}. {item.name} ({value}g)")
      while True:
          try:
              choice = int(input("Select item to sell (0 to cancel): "))
              if choice == 0:
                  return
              if 1 <= choice <= len(self.inventory):
                  item = self.inventory.pop(choice - 1)
                  value = getattr(item, "value", 5)
                  self.gold += value
                  print(f"You sold {item.name} for {value} gold.")
                  print(f"You now have {self.gold} gold.")
                  return
              print("Please select a valid item.")
          except ValueError:
              print("Please enter a number.")


  def use_potion(self):
    if self.healing_potions == 0:
        return False
    else:
      self.hp = min(self.max_hp, self.hp+10)
      self.healing_potions -=1
      return True

  def use_special(self, mob):
    if self.special_cooldown > 0:
        return None
    damage = self.ability_effect(self.attack())
    mob.hp -= damage
    self.special_cooldown = self.ability_cooldown
    return damage

  def reduce_cooldown(self):
    if self.special_cooldown > 0:
      self.special_cooldown -= 1

"""##Monster"""

#Monster
class Mob:
  def __init__(self, name, hp, min_damage, max_damage, xp_reward, mob_type):
    self.name = name
    self.mob_type = mob_type
    self.hp = hp
    self.min_damage = min_damage
    self.max_damage = max_damage
    self.xp_reward = xp_reward
  def attack(self):
    return random.randint(self.min_damage, self.max_damage)

"""##Items"""

#Equipment
class Item:
  def __init__(self, name, slot, hp_bonus=0, min_dmg_bonus=0, max_dmg_bonus=0,value=5):
    self.name = name
    self.slot = slot
    self.hp_bonus = hp_bonus
    self.min_dmg_bonus = min_dmg_bonus
    self.max_dmg_bonus = max_dmg_bonus
    self.value = value

"""#Combat Functions"""

def player_attack(player, mob):
    damage = player.attack()
    mob.hp -= damage
    return damage


def monster_attack(player, mob):
    damage = mob.attack()
    player.hp -= damage
    return damage

def handle_victory(player, mob):
    print(f"{player.name} defeated the {mob.name}!")
    player.xp += mob.xp_reward
    print(f"{player.name} gained {mob.xp_reward} XP!")
    print(f"{player.name} now has a total of {player.xp} XP.")
    player.level_up()

#Combat Function
def Combat(player, mob):
    while player.hp > 0 and mob.hp > 0:
        choice = input(
          f"Choose an action:\n"
          f"1. Attack\n"
          f"2. Use Healing Potion\n"
          f"3. {player.special_ability}"
          f" (CD: {player.special_cooldown})\n"
          f"4. Run\n"
          f"5. Inspect\n"
          )
        if choice == '1':
            player_damage = player_attack(player, mob)
            print(f"{player.name} hits {mob.name} for {player_damage} damage!")
            print(f"{mob.name} HP: {max(0, mob.hp)}\n")
            time.sleep(.4)
            if mob.hp <= 0:
                break
            mob_damage = monster_attack(player, mob)
            print(f"{mob.name} hits {player.name} for {mob_damage} damage!")
            print(f"{player.name} HP: {max(0, player.hp)}\n")
            player.reduce_cooldown()
            time.sleep(.4)

        elif choice == '2':
            if player.use_potion():
                print(f"{player.name} heals for 10 HP!")
                print(f"{player.name} HP: {player.hp}")
                print(f"Potions remaining: {player.healing_potions}\n")
            else:
                print("You have no potions!")
            mob_damage = monster_attack(player, mob)
            print(f"{mob.name} hits {player.name} for {mob_damage} damage!")
            print(f"{player.name} HP: {max(0, player.hp)}\n")
            player.reduce_cooldown()
            time.sleep(.4)

        elif choice == '3':
          damage = player.use_special(mob)
          if damage is None:
              print(
                  f"{player.special_ability} is on cooldown for "
                  f"{player.special_cooldown} more turns.")
              continue
          print(f"{player.name} used {player.special_ability}!")
          print(f"It dealt {damage} damage!")
          if mob.hp <= 0:
            break
          mob_damage = monster_attack(player, mob)
          print(f"{mob.name} hits {player.name} for {mob_damage} damage!")
          print(f"{player.name} HP: {max(0, player.hp)}\n")
          time.sleep(.4)

        elif choice == '4':
            print("You ran away and escaped the dungeon.")
            return "Ran_away"

        elif choice == '5':
            print(
                f"Monster: {mob.name}\n"
                f"Monster HP: {mob.hp}\n"
                f"Monster Type: {mob.mob_type}")

        else:
            print("Please input a valid option.")

    if player.hp > 0:
        handle_victory(player, mob)
        return "Victory"
    print(f"{player.name} was defeated!")
    return "Defeat"

"""#Game Functions"""

def Start_Game():
  global player

  print("Welcome! Let's get started.")
  while True:
    player_name = input("What is your character's name?\n").strip().title()
    if 1 <= len(player_name) <= 15:
      break
    print("Names must be between 1 and 15 characters.")
  # Class Selection
  while True:
      print("\n=== Choose Your Class ===")

      class_names = list(CLASS_DATA.keys())

      for i, (class_name, stats) in enumerate(CLASS_DATA.items(), start=1):
          print(f"\n{i}. {class_name}")
          print(f"   HP Modifier: {stats['hp']:+}")
          print(f"   Min Damage Modifier: {stats['min_damage']:+}")
          print(f"   Max Damage Modifier: {stats['max_damage']:+}")
          print(f"   Starting Potions: +{stats['potions']}")
          print(f"   Special Ability: {stats['ability']}")
          print(f"   Effect: {stats['ability_desc']}")

      choice = input("\nEnter your choice: ")

      try:
          choice = int(choice)

          if 1 <= choice <= len(class_names):
              player_class = class_names[choice - 1]
              break

          print("Please choose a valid class.")

      except ValueError:
          print("Please enter a number.")
  player = Character(player_name, player_class)
  print(f"{player.name} is a brand new {player.player_class} looking to enter the world of adventuring. Good luck!")
  Dungeon_creation(1)

def Dungeon_creation(difficulty):
  print(f"{player.name}, a {player.player_class}, enters the dungeon.")
  floors = difficulty + 1
  floor_count = 1
  while floor_count < floors:
    mob = Spawn_Mob(difficulty)
    print(f"A {mob.name} appeared!")
    time.sleep(1)
    result = Combat(player,mob)
    time.sleep(.5)
    if result == "Defeat" or result == "Ran_away":
      print("Game over.")
      break
    else:
      gold_drop(player,difficulty)
      Handle_Loot(player,mob)
      mob = Spawn_Mob(difficulty)
      print(f"A {mob.name} appeared!")
      time.sleep(1)
      result = Combat(player,mob)
      if result == "Defeat" or result == "Ran_away":
        print("Game over.")
        break
      gold_drop(player,difficulty)
      Handle_Loot(player,mob)
      while True:
        option = input("Continue deeper into the dungeon? Y or N\n").lower()
        if option == "y":
          break
        elif option == "n":
          print("You decide to leave the dungeon.")
          return
        print("Please input Y or N.")
      floor_count += 1
      time.sleep(.5)
      print(f"You descend to the next floor: Floor {floor_count}\n")
      time.sleep(.5)

  if floor_count >= floors and player.hp > 0:
    boss = Spawn_Boss(difficulty)
    print(f"You found the boss! It's a {boss.name}! Prepare to fight.")
    time.sleep(1)
    result = Combat(player, boss)
    time.sleep(.5)
    if result == "Victory":
        gold_drop(player,difficulty)
        Handle_Loot(player, boss)
        Handle_Loot(player, boss)
        print(f"You cleared the dungeon on difficulty {difficulty}.")
        Continue()
    elif result == "Ran_away":
        print("You fled from the boss.")
        print("Game over.")
    else:
        print("Game over.")

"""#Town Functions"""

def Continue():
  while True:
    choice = input("Where would you like to go next?\n1. Shop\n2. Inn\n3. My Character\n4. Dungeon\n5. Retire\n")
    if choice == '1':
      shop(player)

    elif choice == '2':
      if player.gold <5:
        print(f"It costs 5g to rest at the inn. You currently have {player.gold}.")
      else:
        player.gold -= 5
        player.hp = player.max_hp
        print("You spent 5 gold to rest at the inn. You wake up feeling refreshed.")
        print(f"{player.name} is restored to {player.max_hp} health.")

    elif choice == '3':
      while True:
        print("\n=== Character Menu ===")
        print("1. Stats\n2. Equipment\n3. Inventory\n4. Equip from Inventory\n5. Return")
        menu_choice = input('\nWhat would you like to do?' )
        if menu_choice == '1':
          player.view_stats()
        elif menu_choice == '2':
          player.view_equipped()
        elif menu_choice == '3':
          player.view_inventory()
        elif menu_choice == '4':
          player.equip_from_inventory()
        elif menu_choice == '5':
          break
        else:
          print("Please input a valid option.")


    elif choice == '4':
      while True:
        try:
          difficulty = int(input("How difficult of a dungeon do you want to explore? (1-10)"))
          if 1 <= difficulty <= 10:
            Dungeon_creation(difficulty)
            break
          print("Please choose a difficulty between 1 and 10.")
        except ValueError:
          print("Please enter a number between 1 and 10.")

    elif choice == '5':
      print(f"{player.name} decided to end their career as a {player.player_class}. They retired at level {player.level} and lived a peaceful life.")
      print("Game Over")
      break
    else:
      print("Please input a valid option.")

def shop(player):
    shop_items = {
        "1": ("Healing Potion", 5),
        "2": (Item("Wooden Sword", "Weapon", min_dmg_bonus=2, max_dmg_bonus=5, value=10), 15),
        "3": (Item("Leather Cap", "Helmet", hp_bonus=10, value=10), 15),
        "4": (Item("Leather Shirt", "Chest", hp_bonus=15, value=15), 20),
        "5": (Item("Leather Shoes", "Boots", hp_bonus=5, value=8), 10)
    }

    while True:
        print("\n--- Shop ---")
        print("1. Buy Items")
        print("2. Sell Items")
        print("3. Exit Shop")

        shop_choice = input("What would you like to do?\n")

        if shop_choice == "1":
            while True:
                print("\nThe shop's inventory:")
                for key, (item, price) in shop_items.items():
                    if item == "Healing Potion":
                        print(f"{key}. {item} - {price}g")

                    else:
                        print(
                            f"{key}. {item.name} | "
                            f"HP +{item.hp_bonus} | "
                            f"Min DMG +{item.min_dmg_bonus} | "
                            f"Max DMG +{item.max_dmg_bonus} | "
                            f"{price}g"
                        )

                print(f"\nYou currently have {player.gold} gold.")

                choice = input("Select an item to buy or X to go back.\n").lower()
                if choice == "x":
                    break

                if choice not in shop_items:
                    print("Please select a valid option.")
                    continue
                item, price = shop_items[choice]

                if player.gold < price:
                    print("You don't have enough gold.")
                    continue
                player.gold -= price

                if item == "Healing Potion":
                    player.healing_potions += 1

                    print(f"You bought a healing potion. "
                        f"You now have {player.healing_potions} potions.")

                else:
                    equip_choice = input(f"You purchased a {item.name}. Equip it now? (Y/N)\n").lower()
                    if equip_choice == "y":
                        player.equip(item)
                    else:
                        player.inventory.append(item)
                        print(f"{item.name} was added to your inventory.")
                print(f"You have {player.gold} gold remaining.")

        elif shop_choice == "2":
            player.sell_item()

        elif shop_choice == "3":
            print("You leave the shop.")
            return
        else:
            print("Please input a valid option.")

"""#Monster and Loot Tables"""

def Spawn_Mob(difficulty):      #name, hp, min_damage, max_damage, xp_reward, mob_type
  monsters = [
    ("Goblin", 10, 1, 5, 1,"Humanoid"),
    ("Wolf", 15, 2, 6, 1, "Beast"),
    ("Bandit Fighter", 20, 3, 5, 2, "Humanoid"),
    ("Rat", 10, 1, 4, 1, "Beast"),
    ("Imp", 10, 3, 4, 1, "Demon"),
    ("Bandit Archer", 15, 5, 6, 2, "Human"),
    ("Giant Spider", 12, 2, 5, 1, "Beast"),
    ("Boar", 20, 1, 5, 2, "Beast"),
    ("Lesser Drake", 18, 2, 6, 2, "Dragonkin")
  ]
  monster = random.choice(monsters)
  return Mob(monster[0],
      monster[1] + (difficulty-1) * 3,
      monster[2] + (difficulty-1),
      monster[3] + (difficulty-1),
      monster[4] + (difficulty-1),
      monster[5])

def Spawn_Boss(difficulty):     #name, hp, min_damage, max_damage, xp_reward, mob_type
  bosses = [
    ("Bandit Leader", 45, 4, 7, 4,"Humanoid"),
    ("Alpha Wolf", 35, 4, 8, 4, "Beast"),
    ("Goblin Leader", 35, 2, 8, 4, "Humanoid"),
    ("Troll", 55, 2, 6, 4, "Humanoid"),
    ("Baby Dragon", 60, 3, 10, 5, "Dragonkin")
  ]
  boss = random.choice(bosses)
  return Mob(boss[0],
      boss[1] + (difficulty-1) * 5,
      boss[2] + (difficulty-1),
      boss[3] + (difficulty-1),
      boss[4] + (difficulty-1) * 2,
      boss[5])

def Loot_Drop():
  loot_table = [
      Item("Sharp Stick", "Weapon", min_dmg_bonus=1),
      Item("Rusty Sword", "Weapon", min_dmg_bonus=2, max_dmg_bonus=3),
      Item("Paper Hat", "Helmet", hp_bonus=1),
      Item("Thin Shirt", "Chest", hp_bonus=2),
      Item("Mocassins", "Boots", hp_bonus=1)
  ]


  random_num = random.random()
  if random_num < 0.25:
    return random.choice(loot_table)
  elif random_num < 0.5:
    return "Healing potion"
  return None

def Handle_Loot(player,mob):
  loot = Loot_Drop()
  if loot:
    if loot == "Healing potion":
      player.healing_potions += 1
      print(f"You found a healing potion! You now have {player.healing_potions} potions.")
    else:
      print(f"The {mob.name} dropped a {loot.name}!")
      choice = input("Equip it? Y or N\n").lower()
      if choice == "y":
        player.equip(loot)
      else:
        player.inventory.append(loot)
        print(f"{loot.name} was added to your inventory.")

def gold_drop(player,difficulty):
  gold_found = random.randint(1+(difficulty-1), difficulty * 3)
  player.gold += gold_found
  print(f"You found {gold_found} gold! "
        f"You now have {player.gold} gold.")

"""#Game Testing"""
if __name__ == "__main__":
    Start_Game()

