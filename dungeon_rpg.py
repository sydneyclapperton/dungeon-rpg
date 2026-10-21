#packages
import random
import json

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
                "ability_effect": lambda x, player : x * 2,
                "crit_chance": 0.05,
                "class_desc": "A seasoned fighter with high health and reliable damage"},
  "Mage" : {"hp": -10,
              "min_damage":3,
              "max_damage":5,
              "potions":3,
              "ability": "Fireball",
              "cooldown": 3,
              "ability_desc": "Adds damage to attack based on level",
              "ability_effect": lambda x, player : x + 15 + (player.level-1)*4,
              "crit_chance": 0.12,
              "class_desc": "A fragile spellcaster who relies on powerful magic"},
  "Rogue" : {"hp": 0,
              "min_damage":0,
              "max_damage":7,
              "potions":1,
              "ability": "Knife Throw",
              "cooldown": 3,
              "ability_desc": "Doubles attack damage and adds 5",
              "ability_effect": lambda x, player : x*2 + 5,
              "crit_chance": 0.2,
              "class_desc": "A nimble assassin who excels at critical strikes"},
  "Paladin" : {"hp": 30,
            "min_damage":1,
            "max_damage":2,
            "potions":2,
            "ability": "Smite",
            "cooldown": 2,
            "ability_desc": "Adds damage to attack based on level",
            "ability_effect": lambda x, player : x + 10 +(player.level-1)*3,
            "crit_chance": 0.09,
            "class_desc": "A holy warrior with exceptional durability"},
    "Commoner" : {"hp": -10,
                "min_damage":0,
                "max_damage": -1,
                "potions":0,
                "ability": "Throw Rock",
                "cooldown": 4,
                "ability_desc": "Adds 2 damage to attack",
                "ability_effect": lambda x, player : x + 2,
                "crit_chance": 0.01,
                "class_desc": "An ordinary person who made several bad decisions and somehow ended up in a dungeon"},
}

#Object Creation
#Character
class Character:
  def __init__(self,name,player_class):
    self.name = name
    self.player_class = player_class
    self.level = 1
    self.xp = 0
    self.max_hp = 40
    self.hp = self.max_hp
    self.min_damage = 1
    self.max_damage = 6
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
    self.crit_chance = class_bonus.get("crit_chance", 0)
    self.highest_floor = 1
    self.run_stats = {
      "kills": 0,
      "elite_kills":0,
      "boss_kills": 0,
      "xp_earned": 0,
      "gold_earned": 0,
      "items_found": 0}
    self.signature = None
    self.signature_cd = 0

  def attack(self):
    damage = random.randint(self.min_damage, self.max_damage)
    crit = random.random() < self.crit_chance
    if crit:
      damage *= 2
    return damage, crit

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

  def level_up(self):
    xp_needed = self.level * 10
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

  def view_stats(self):
    signature_text = ""
    if self.signature:
        signature_text = f"Signature Move: {self.signature}\n"
    
    return (f"Name: {self.name}\nClass: {self.player_class}\n"
          f"Level: {self.level}\nAbility: {self.special_ability}\n"
          f"Effect: {self.ability_desc}\n"
          f"{signature_text}"
          f"Current XP: {self.xp}/{self.level*10}\n\n"
          f"Highest Floor Cleared: {self.highest_floor}\n\n"
          f"HP: {self.hp}/{self.max_hp}\n"
          f"Damage: {self.min_damage}-{self.max_damage}\n\n"
          f"Gold: {self.gold}\n"
          f"Potions: {self.healing_potions}\n"
          )

  def use_potion(self):
    if self.healing_potions == 0:
        return False
    else:
      heal_amount = int(self.max_hp*.4)
      self.hp = min(self.max_hp, self.hp+heal_amount)
      self.healing_potions -=1
      return heal_amount

  def use_special(self, mob):
    if self.special_cooldown > 0:
        return None
    damage, crit = self.attack()
    damage = self.ability_effect(damage, self)
    mob.hp -= damage
    self.special_cooldown = self.ability_cooldown
    return damage, crit

  def reduce_cooldown(self):
    if self.special_cooldown > 0:
      self.special_cooldown -= 1
    if self.signature_cd > 0:
      self.signature_cd -= 1
  
  def use_signature(self, mob):
      if self.signature_cd > 0:
        return None
      elif self.signature == "Rejuvenation":
        self.signature_cd = 5
        heal_amount = int(self.max_hp*.7)
        self.hp = min(self.hp+heal_amount, self.max_hp)
        return {
          "damage": 0,
          "heal" : heal_amount,
          "instakill": False}
      
      elif self.signature == "Reckoning":
        self.signature_cd = 6
        if mob.mob_type in ["Demon", "Undead"]:
          mob.hp = 0
          return {
            "damage": 0,
            "heal" : 0,
            "instakill": True}
        damage, crit = self.attack()
        damage *= 2.5
        actual_damage = min(int(damage), mob.hp)
        mob.hp -= actual_damage
        return {
          "damage": actual_damage,
          "heal" : 0,
          "instakill": False}

      elif self.signature == "Bloodlust":
        self.signature_cd = 5
        damage, crit = self.attack()
        actual_damage = min(damage*2, mob.hp)
        healed = int(actual_damage/2)
        self.hp = min(self.hp + healed, self.max_hp)
        mob.hp -= actual_damage
        return {
          "damage": actual_damage,
          "heal" : healed,
          "instakill": False}

"""##Monster"""

#Monster
class Mob:
  def __init__(self, name, hp, min_damage, max_damage, xp_reward, mob_type, ability_name=None, ability_effect = None, cooldown=0):
    self.name = name
    self.mob_type = mob_type
    self.hp = hp
    self.max_hp = hp
    self.min_damage = min_damage
    self.max_damage = max_damage
    self.xp_reward = xp_reward
    self.ability_name = ability_name
    self.ability_effect = ability_effect
    self.cooldown = 0
    self.ability_cooldown = cooldown
  def attack(self):
    return random.randint(self.min_damage, self.max_damage)

  def reduce_cooldown(self):
    if self.cooldown > 0:
        self.cooldown -= 1

  def use_ability(self,target):
    if self.ability_effect is None:
      return None
    elif self.cooldown > 0:
      return None
    else:
      self.cooldown = self.ability_cooldown
      return self.ability_effect(target)
"""##Items"""

#Equipment
class Item:
  def __init__(self, name, slot, hp_bonus=0, min_dmg_bonus=0, max_dmg_bonus=0,value=5, enhancement=0):
    self.name = name
    self.slot = slot
    self.hp_bonus = hp_bonus
    self.min_dmg_bonus = min_dmg_bonus
    self.max_dmg_bonus = max_dmg_bonus
    self.value = value
    self.enhancement = enhancement

"""#Combat Functions"""

def handle_victory(player, mob, difficulty):
    player.xp += mob.xp_reward
    leveled_up = player.level_up()
    gold_found = random.randint(1+(difficulty-1), 3*difficulty)
    player.run_stats["kills"] += 1
    # Boss bonus
    if difficulty % 5 == 0:
        gold_found *= 2
        loot = Loot_Drop("boss",difficulty)
        player.run_stats["boss_kills"] += 1
    elif getattr(mob, "is_elite", False):
        gold_found *= 2
        loot = Loot_Drop("elite",difficulty)
        player.run_stats["elite_kills"] += 1
    else:
      loot = Loot_Drop("basic", difficulty)
    if loot:
        player.run_stats["items_found"] += 1
        if loot == "Healing potion":
            player.healing_potions += 1
        else:
            player.inventory.append(loot)
    player.gold += gold_found
    player.run_stats["xp_earned"] += mob.xp_reward
    player.run_stats["gold_earned"] += gold_found
    return {
        "xp_gained": mob.xp_reward,
        "gold_found": gold_found,
        "loot": loot,
        "leveled_up": leveled_up}

"""#Monster and Loot Tables"""
monsters = [
  ("Goblin", 10, 1, 5, 1,"Humanoid"),
  ("Wolf", 15, 2, 6, 1, "Beast"),
  ("Bandit Fighter", 20, 3, 5, 2, "Humanoid"),
  ("Rat", 10, 1, 4, 1, "Beast"),
  ("Imp", 10, 3, 4, 1, "Demon"),
  ("Bandit Archer", 15, 5, 6, 2, "Human"),
  ("Giant Spider", 12, 2, 5, 1, "Beast"),
  ("Boar", 20, 1, 5, 2, "Beast"),
  ("Lesser Drake", 18, 2, 6, 2, "Dragonkin"),
  ("Skeleton", 15, 2, 5, 2, "Undead")
  ]
bosses = [
    ("Bandit Leader", 45, 4, 7, 4,"Humanoid", "Backstab", lambda x: x*2, 3),
    ("Alpha Wolf", 35, 4, 8, 4, "Beast", "Dire Fang", lambda x: x+10, 4),
    ("Goblin Leader", 35, 2, 8, 4, "Humanoid", "Throw Rock", lambda x: x+5, 3),
    ("Troll", 55, 2, 6, 4, "Humanoid", "Throw Boulder", lambda x: x+20, 5),
    ("Baby Dragon", 60, 3, 10, 5, "Dragonkin", "Fire Breath", lambda x: x*3 - 5, 4),
    ("Giant Python", 60, 7, 15, 10, "Beast", "Constrict", lambda x: x*2 + 2, 3),
    ("Lesser Fiend", 50, 6, 10, 8, "Demon", "Shadow Strike", lambda x: x+15, 4)
  ]
def Spawn_Mob(difficulty):    #name, hp, min_damage, max_damage, xp_reward, mob_type, ability_name=None, ability_effect = None, cooldown=0
  monster = random.choice(monsters)
  mob = Mob(monster[0],
      monster[1] + (difficulty-1) * 4,
      monster[2] + (difficulty-1),
      monster[3] + (difficulty-1) * 2,
      monster[4] + (difficulty-1),
      monster[5])
  mob.is_elite = False
  if random.random() < 0.1:
      mob.is_elite = True
      mob.name = f"Elite {mob.name}"
      mob.max_hp *= 2
      mob.hp = mob.max_hp
      mob.min_damage += difficulty // 2
      mob.max_damage += difficulty
      mob.xp_reward *= 2
  return mob

def Spawn_Boss(difficulty):   #name, hp, min_damage, max_damage, xp_reward, mob_type, ability_name=None, ability_effect = None, cooldown=0
  boss = random.choice(bosses)
  return Mob(boss[0],
      boss[1] + (difficulty-1) * 5,
      boss[2] + (difficulty-1) * 2,
      boss[3] + (difficulty-1) * 3,
      boss[4] + (difficulty-1),
      boss[5],
      boss[6],
      boss[7],
      boss[8])
#Loot tables
basic_loot_table = [
        Item("Sharp Stick", "Weapon", min_dmg_bonus=1),
        Item("Rusty Sword", "Weapon", min_dmg_bonus=2, max_dmg_bonus=3),
        Item("Paper Hat", "Helmet", hp_bonus=1),
        Item("Thin Shirt", "Chest", hp_bonus=2),
        Item("Mocassins", "Boots", hp_bonus=1),
        Item("Used Wizard Robes", "Chest", hp_bonus = -5, min_dmg_bonus= 1, max_dmg_bonus=3),
        Item("Smelly Leather Shoes", "Boots", hp_bonus = 5, min_dmg_bonus= -1),
        Item("Bucket", "Helmet", hp_bonus = 10, min_dmg_bonus =-1, max_dmg_bonus = -3)
    ]
boss_loot_table= [
        Item("Dragon Tooth", "Weapon", min_dmg_bonus=4, max_dmg_bonus=7),
        Item("Flaming Sword", "Weapon", min_dmg_bonus=3, max_dmg_bonus=10),
        Item("Dragonscale Helmet", "Helmet", hp_bonus=10),
        Item("Dragonscale Shirt", "Chest", hp_bonus=20),
        Item("Dragonscale Boots", "Boots", hp_bonus=10)
    ]
elite_loot_table =[
        Item("Iron Sword", "Weapon", min_dmg_bonus=3, max_dmg_bonus=5),
        Item("Iron Helmet", "Helmet", hp_bonus=7),
        Item("Iron Breastplate", "Chest", hp_bonus=17),
        Item("Iron Boots", "Boots", hp_bonus=7)]
shop_loot_table = [
  Item("Bronze Sword", "Weapon", min_dmg_bonus=2, max_dmg_bonus=5, value=25),
  Item("Magic Wand", "Weapon", min_dmg_bonus=1, max_dmg_bonus=8, value=25),
  Item("Leather Cap", "Helmet", hp_bonus=5, value=15),
  Item("Leather Shirt", "Chest", hp_bonus=15, value=30),
  Item("Leather Boots", "Boots", hp_bonus=5, value=15),
  Item("Steel Longblade", "Weapon", min_dmg_bonus=10, max_dmg_bonus=20, value= 250)
  ]
def Loot_Drop(loot_type, floor):
  if loot_type == "basic":
    random_num = random.random()
    if random_num < 0.25:
      return enhance_item(random.choice(basic_loot_table), floor)
    elif random_num < 0.5:
      return "Healing potion"
  elif loot_type =="elite":
    if random.random() < .7:
      return enhance_item(random.choice(elite_loot_table),floor)
    else:
      return "Healing potion"
  elif loot_type =="boss":
    return enhance_item(random.choice(boss_loot_table),floor)
  return None

def enhance_item(item,floor):
  min_bonus = floor//10
  max_bonus = min_bonus*2 + 2
  enhancement = random.randint(min_bonus,max_bonus)
  return Item(
    item.name,
    item.slot,
    hp_bonus=item.hp_bonus + (enhancement * 5),
    min_dmg_bonus=item.min_dmg_bonus + enhancement,
    max_dmg_bonus=item.max_dmg_bonus + (enhancement * 2),
    value=item.value + (enhancement * 5),
    enhancement=enhancement)

#Save Game
def save_game(player):
    return {
        "name": player.name,
        "player_class": player.player_class,
        "level": player.level,
        "xp": player.xp,
        "hp": player.hp,
        "gold": player.gold,
        "healing_potions": player.healing_potions,
        "highest_floor" : player.highest_floor,
        "run_stats": player.run_stats,
        "signature": player.signature,
        "signature_cd": player.signature_cd,
        "equipment": {
            slot: {"name": item.name, "enhancement": item.enhancement} if item else None
            for slot, item in player.equipment.items()},
        "inventory": [ {"name": item.name,"enhancement": item.enhancement} for item in player.inventory]
    }

#Load Game
def load_game(uploaded_file):
  return json.load(uploaded_file)

#Item lookup
def get_item_by_name(name):
    for item in basic_loot_table + elite_loot_table + boss_loot_table + shop_loot_table:
        if item.name == name:
            return item
    return None

def create_enhanced_item(base_item, enhancement):
    return Item(
        base_item.name,
        base_item.slot,
        hp_bonus=base_item.hp_bonus + (enhancement * 5),
        min_dmg_bonus=base_item.min_dmg_bonus + enhancement,
        max_dmg_bonus=base_item.max_dmg_bonus + (enhancement * 2),
        value=base_item.value+(enhancement * 5),
        enhancement=enhancement
    )

def get_unlocked_floors(highest_floor):
    unlocked = [1]
    checkpoint = 11
    while checkpoint <= highest_floor + 1:
        unlocked.append(checkpoint)
        checkpoint += 10
    return unlocked