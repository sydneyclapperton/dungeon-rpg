# Dungeon RPG

A browser-based RPG built with Python and Streamlit featuring dungeon exploration, turn-based combat, character classes, equipment progression, boss encounters, save/load functionality, and dungeon run tracking.

Players create a character, choose a class, and venture into an increasingly dangerous dungeon filled with monsters, powerful bosses, and valuable loot. Defeat enemies, gain experience, level up, discover new equipment, and see how far your adventurer can go before retiring or falling in battle.

[Play Dungeon RPG](https://dungeon-rpg-sydney.streamlit.app/)

---

## Features

### Character System

- Create a custom character
- Choose a character name and class
- Six playable classes:
  - Warrior
  - Mage
  - Rogue
  - Paladin
  - Berserker
  - Commoner
- Class-specific combat abilities
- Character leveling system
- Full heal on level up
- Character stats displayed in the sidebar
- Equipment displayed in the sidebar

### Combat System

- Turn-based combat
- Randomized damage rolls
- Critical hit system
- Class abilities with cooldowns
- Signature Move system
- Healing potion system
- Enemy abilities and cooldowns
- Combat log displaying battle events
- Visual HP bars for player and enemy health

### Dungeon System

- Multi-floor dungeon progression
- Enemy scaling based on floor level
- Random monster encounters
- Elite monster encounters
- Boss encounters every 5 floors
- Boss-specific abilities
- Boss reward bonuses
- Random dungeon events
- Treasure chest encounters
- Healing fountain encounters
- Shrine encounters
- Trap encounters
- Floor checkpoint system
- Unlockable starting floors
- Progress persists between saves

## Random Dungeon Events

Dungeon exploration may trigger special events instead of combat.

Current events include:

- Treasure Chest
  - Open the chest for a reward or leave it untouched
  - Possible rewards include gold, potions, and equipment
  - Rare trapped chests may deal damage

- Healing Fountain
  - Restore 50% of your maximum health
  - May be ignored if healing is not needed

- Shrine
  - Choose one blessing:
    - Gold
    - Experience
    - Full healing
    - Equipment enhancement

- Trap
  - Attempt to dodge the trap or brace for impact
  - Rogues automatically detect and avoid traps

### Loot & Equipment

- Random loot drops
- Guaranteed boss loot
- Equipment slots:
  - Weapon
  - Helmet
  - Chest
  - Boots
- Equipment grants stat bonuses
- Elite-specific loot table
- Increased rewards from elite enemies
- Equipment swapping
- Inventory management
- Item selling system
- Item enhancement system
- Item enhancements scale based on dungeon depth
- Enhanced items provide increased stats and value
- Enhanced items persist through save/load

### Progression & Economy

- Experience (XP) rewards
- Gold rewards from combat
- Bonus gold from boss encounters
- Shop system
- Potion purchasing
- Item selling
- Blacksmith equipment upgrades
- Enhancement costs scale with item level
- Inn for healing and recovery
- Quest system
- Quest rewards
- Quest Board with rotating objectives
- Highest Floor Cleared tracking
- Unlockable checkpoint progression

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
- Lesser Fiend

Bosses feature:

- Increased stats
- Unique combat abilities
- Bonus rewards
- Guaranteed boss loot

---

## Monster Types

Current monster families include:

- Humanoids
- Beasts
- Demons
- Undead

Special interactions:

- Reckoning instantly purges Demons and Undead

---

## Elite Monsters

Some dungeon encounters may spawn Elite Monsters.

Elite Monsters feature:

- Increased health
- Increased damage
- Increased XP rewards
- Increased gold rewards
- Elite-specific loot drops

Elite kills are tracked in run statistics and summaries.

---

### Town Hub

- Shop
- Sell equipment
- Inn
- Blacksmith
- Inventory management
- Trainer
- Quest Board
- Dungeon floor selection
- Save game
- Retire character

### Blacksmith

- Upgrade equipped items and inventory gear
- Increase item enhancement levels
- Upgrade costs scale with enhancement level
- Enhanced items gain additional stats and value

### Trainer System

Unlocks at Level 10.
Players can visit the Trainer to learn powerful Signature Moves. Only one Signature Move can be known at a time, but abilities may be retrained for gold.
Current Signature Moves:
- Rejuvenation
  - Restore 70% of maximum HP
- Bloodlust
  - Deal double damage and heal for 50% of damage dealt
- Reckoning
  - Heavy damage attack
  - Instantly purges Demons and Undead
- Greed
  - Deal normal damage
  - Killing blows grant bonus Gold and XP

### Quest System

Players can visit the Quest Board in town to accept challenges for additional rewards.

Features include:

- Rotating quest board
- Up to 3 active quests at a time
- Progress tracked from quest acceptance
- Turn-in system for completed quests
- Gold and XP quest rewards

Current quest types include:

- Monster Hunter
  - Defeat monsters

- Elite Hunter
  - Defeat elite monsters

- Boss Slayer
  - Defeat bosses

- Boss Hunter
  - Defeat multiple bosses

- Deep Delver
  - Reach deeper dungeon floors

- Gold Hoarder
  - Earn gold

- Treasure Seeker
  - Find equipment and loot

### Save & Load System

- Downloadable save files
- Upload save files to continue existing characters
- Save data includes:
  - Character information
  - Level and XP
  - Current HP
  - Gold
  - Potions
  - Equipped gear
  - Inventory contents
  - Highest floor cleared
  - Run statistics
  - Learned Signature Move
  - Signature cooldown state
  - Item enhancement data
  - Active quests
  - Quest board data
- Works on desktop and mobile devices
- No account required

### Run Tracking

- Dungeon run statistics
- Monsters defeated
- Elite monsters defeated
- Bosses defeated
- XP earned
- Gold earned
- Items found
- Career Summary upon retirement
- Life Summary upon death
- Highest cleared floor

---

## Technologies Used

- Python 3
- Streamlit
- Object-Oriented Programming (OOP)
- JSON save files
- Python `random` module

---

## Planned Features

- Additional character classes
- More monsters and bosses
- Additional Signature Moves
- Expanded boss mechanics
- Additional equipment sets
- Loot rarity system
- Additional Quests
- Status effects (Poison, Burn, Stun, etc.)
- Achievements and records
- Monster artwork
- Multiple dungeon regions
- Dungeon-specific loot tables
