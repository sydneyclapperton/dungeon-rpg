import random

quest_pool =[{
    "name": "Monster Hunter",
    "description": "Defeat 10 monsters.",
    "target": "kills",
    "goal": 10,
    "reward_type": "Gold",
    "reward_amount": 100
    },
    {
    "name": "Elite Hunter",
    "description": "Defeat 3 elite monsters.",
    "target": "elite_kills",
    "goal": 3,
    "reward_type": "XP",
    "reward_amount": 50
    },
    {
    "name": "Boss Slayer",
    "description": "Defeat 1 bosses.",
    "target": "boss_kills",
    "goal": 1,
    "reward_type": "XP",
    "reward_amount": 50
    },
    {
    "name": "Boss Hunter",
    "description": "Defeat 3 bosses.",
    "target": "boss_kills",
    "goal": 3,
    "reward_type": "Gold",
    "reward_amount": 500
    },
    {
    "name": "Deep Delver",
    "description": "Delve 5 floors deeper into the dungeon.",
    "target": "highest_floor",
    "goal": 5,
    "reward_type": "Gold",
    "reward_amount": 500
    },
    {
    "name": "Gold Hoarder",
    "description": "Earn 250 gold.",
    "target": "gold_earned",
    "goal": 250,
    "reward_type": "XP",
    "reward_amount": 50
    },
    {
    "name": "Treasure Seeker",
    "description": "Find 5 items.",
    "target": "items_found",
    "goal": 5,
    "reward_type": "Gold",
    "reward_amount": 150
    }
]

def get_available_quests(count=3):
    return random.sample(quest_pool, count)

def accept_quest(player, quest_template):
    quest = quest_template.copy()
    if quest["target"] == "highest_floor":
        quest["starting_value"] = player.highest_floor
    else:
        quest["starting_value"] = player.run_stats[quest["target"]]
    return quest

def get_quest_progress(player,quest):
    if quest["target"] == "highest_floor":
        current = player.highest_floor
    else:
        current = player.run_stats[quest["target"]]
    return current - quest["starting_value"]

def is_quest_complete(player, quest):
    return get_quest_progress(player, quest) >= quest["goal"]

def grant_quest_reward(player, quest):
    if quest["reward_type"] == "Gold":
        player.gold += quest["reward_amount"]
    elif quest["reward_type"] == "XP":
        player.xp += quest["reward_amount"]
        player.run_stats["xp_earned"] += quest["reward_amount"]
        player.level_up()

