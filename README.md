# Dungeon RPG

A text-based RPG built in Python and Streamlit featuring dungeon exploration, turn-based combat, character classes, equipment progression, boss encounters, and dungeon run tracking.

Players create a character, choose a class, and venture into an increasingly dangerous dungeon filled with monsters, powerful bosses, and valuable loot. Defeat enemies, gain experience, level up, find equipment upgrades, and see how far your adventurer can go before retiring or falling in battle.

---

## Features

### Character System

- Create a custom character
- Choose a character name and class
- Four playable classes:
  - Warrior
  - Mage
  - Rogue
  - Paladin
- Class-specific combat abilities
- Character leveling system
- Full heal on level up
- Character stats displayed in a sidebar

### Combat System

- Turn-based combat
- Randomized damage rolls
- Class abilities with cooldowns
- Healing potion system
- Enemy abilities and cooldowns
- Combat log displaying battle events

### Dungeon System

- Multi-floor dungeon progression
- Enemy scaling based on floor level
- Random monster encounters
- Boss encounters every 5 floors
- Boss-specific abilities
- Boss reward bonuses

### Loot & Equipment

- Random loot drops
- Guaranteed boss loot
- Equipment slots:
  - Weapon
  - Helmet
  - Chest
  - Boots
- Equipment grants stat bonuses
- Inventory management
- Item equipping and swapping

### Progression & Economy

- Experience (XP) rewards
- Gold rewards from combat
- Bonus gold from boss encounters
- Shop system
- Potion purchasing
- Item selling system
- Inn for healing and recovery

### Run Tracking

- Dungeon run statistics
- Monsters defeated
- Bosses defeated
- XP earned
- Gold earned
- Items found
- Career Summary upon retirement
- Life Summary upon death

### Town Hub

- Shop
- Sell equipment
- Inn
- Inventory management
- Enter dungeon
- Retire character

---

## Boss Encounters

Every 5th floor contains a boss encounter.

Current bosses include:

- Bandit Leader
- Alpha Wolf
- Goblin Leader
- Troll
- Baby Dragon
- Giant Python

Bosses feature:

- Increased stats
- Unique combat abilities
- Bonus rewards
- Guaranteed boss loot

---

## Technologies Used

- Python 3
- Streamlit
- Object-Oriented Programming (OOP)
- Python `random` module

---

## Planned Features

- Save/load system
- Additional character classes
- More monsters and bosses
- Expanded boss mechanics
- Additional equipment sets
- Loot rarity system
- Status effects (Poison, Burn, Stun, etc.)
- Elite enemies
- Achievements and records

---

## How to Run

Install Streamlit:

```bash
pip install streamlit
