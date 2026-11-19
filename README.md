# Dungeon RPG

A browser-based RPG built with Python and Streamlit featuring multi-dungeon exploration, character progression, equipment enhancement, quests, random events, boss encounters, and persistent save/load functionality.

Players create a character, choose a class, and venture into increasingly dangerous dungeons filled with monsters, elite enemies, powerful bosses, and unique rewards. Defeat enemies, gain experience, level up, enhance equipment, learn Signature Moves, complete quests, unlock new dungeons, and build a legendary adventurer before eventually retiring or falling in battle.

[Play Dungeon RPG](https://dungeon-rpg-sydney.streamlit.app/)

---

## Features

### Character System

- Create a custom character
- Choose a character name and class
- Seven playable classes:
  - Warrior
  - Mage
  - Rogue
  - Paladin
  - Berserker
  - Ranger
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
- Enemy trait system
- Combat log displaying battle events
- Visual HP bars for player and enemy health

### Dungeon System

- Multiple unique dungeons
- Dungeon-specific progression tracking
- Dungeon unlock system
- Multi-floor dungeon progression
- Enemy scaling based on floor level
- Random monster encounters
- Elite monster encounters
- Random monster traits
- Boss encounters every 5 floors
- Dungeon-specific final bosses
- Dungeon-specific reward tables
- Dungeon-specific environmental effects
- Random dungeon events
- Treasure chest encounters
- Healing fountain encounters
- Shrine encounters
- Trap encounters
- Floor checkpoint system
- Unlockable starting floors
- Progress persists between saves

### Legacy System

- Persistent account-wide progression
- Hall of Heroes tracking retired and fallen adventurers
- Permanent dungeon unlock progression
- Permanent Trainer unlocks
- Bank storage shared across heroes
- Achievement tracking across generations
- Legacy data persists through save/load

### Achievement System

- Persistent achievement tracking
- Unlock notifications
- Achievement collection view
- Boss achievements
- Level milestone achievements
- Retirement achievements
- Death achievements
- Dungeon completion achievements

## Current Dungeons

### The Ancient Depths

The first dungeon available to all adventurers.

Features:

- Mixed monster population
- Elite encounters
- Boss encounters every 5 floors
- Final Boss: Ancient Dragon

### Frostbound Sanctum

Unlocked by clearing The Ancient Depths.

Features:

- Frozen-themed monsters and bosses
- Elementals, Constructs, Undead, Dragonkin, and Beasts
- Final Boss: The Frostbinder
 
### Crypt of the Damned

Unlocked by clearing Frostbound Sanctum.

Features:

- Undead-themed monsters and bosses
- Necrotic Aura environmental effect
- Skeletons, Wraiths, Necromancers, Zombies, and other undead enemies
- Final Boss: Bone Tyrant

## Dungeon Environments

Each dungeon features unique environmental effects that alter gameplay.

### Ancient Depths

- No environmental modifier

### Frostbound Sanctum

- Bitter Cold
- Healing effects reduced by 25%

### Crypt of the Damned

- Necrotic Aura
- Take damage at the end of each turn equal to the current floor level

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
  - Ring
  - Necklace
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
- Equipment stat comparison system
- Green/red stat comparison indicators

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
- Per-dungeon progression tracking
- Per-dungeon clear tracking
- Total dungeon clear tracking
- Dungeon-specific rewards
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
- Lich
- and more!

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
- Dragonkin
- Constructs
- Elementals

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

## Monster Traits

Some monsters may spawn with special traits, creating more dangerous or rewarding encounters.

Current traits include:

- Enraged
  - Increased damage

- Tough
  - Increased health

- Rich
  - Increased gold rewards

Traits can also appear on Elite Monsters.

---

### Town Hub

- Shop
- Sell equipment
- Inn
- Blacksmith
- Inventory management
- Trainer
- Bank
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
  - Dungeon progression
  - Dungeon clear counts
  - Highest floor per dungeon
  - Run statistics
  - Learned Signature Move
  - Signature cooldown state
  - Item enhancement data
  - Active quests
  - Quest board data
  - Legacy progression data
  - Hall of Heroes records
  - Achievement progress
  - Banked gold
  - Permanent unlocks
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
- Per-dungeon progression
- Per-dungeon clears
- Total dungeon clears

---

## Technologies Used

- Python 3
- Streamlit
- Object-Oriented Programming (OOP)
- JSON save files
- Python `random` module

---

## Planned Features

- Additional dungeons
- Additional dungeon environments
- Achievement rewards
- Subclass system
- Hall of Legends
- Additional character classes
- Expanded boss mechanics
- Additional Signature Moves
- Additional quest varieties
- Arena game mode
- Status effects (Poison, Burn, Stun, etc.)
- Additional necklace effects
- Loot rarity system
- Monster artwork
