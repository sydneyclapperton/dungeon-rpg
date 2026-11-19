DEFAULT_LEGACY_DATA ={
    "bank_gold": 0,
    "highest_unlocked_dungeon": 1,
    "trainer_unlocked": False,
    "hall_of_heroes": [],
    "achievements": []
}


def has_achievement(legacy_data, achievement_id):
    return achievement_id in legacy_data["achievements"]

def unlock_achievement(legacy_data, achievement_id):
    if achievement_id not in legacy_data["achievements"]:
        legacy_data["achievements"].append(achievement_id)
        return True
    return False


ACHIEVEMENTS = {
    "first_blood": {
        "name": "First Blood",
        "description": "Defeat your first monster."
    },
    "boss_slayer":{
        "name": "Boss Slayer",
        "description": "Defeat your first boss."
    },
    "first_death": {
        "name": "R.I.P.",
        "description": "Rest in pieces..."
    },
    "dragon_slayer": {
        "name": "Dragon Slayer",
        "description": "Defeat The Ancient Dragon."
    },
    "frozen_conqueror": {
        "name": "Frozen Conqueror",
        "description": "Defeat The Frostbinder."
    },
    "bone_collector": {
        "name": "Bone Collector",
        "description": "Defeat The Bone Tyrant."
    },
    "newbie": {
        "name": "New Adventurer",
        "description": "Reach level 5 for the first time."
    },
    "noteworthy": {
        "name": "Noteworthy Adventurer",
        "description": "Reach level 10 for the first time."
    },
    "experienced": {
        "name": "Experienced Adventurer",
        "description": "Reach level 25 for the first time."
    },
    "veteran": {
        "name": "Veteran Adventurer",
        "description": "Reach level 40 for the first time."
    },
    "renowned": {
        "name": "Renowned Adventurer",
        "description": "Reach level 50 for the first time."
    },
    "first_retirement": {
        "name": "A Life Well Lived",
        "description": "Retire your first hero."
    }
}

LEVEL_ACHIEVEMENTS = [
    (5, "newbie"),
    (10, "noteworthy"),
    (25, "experienced"),
    (40, "veteran"),
    (50, "renowned")
]

DUNGEON_CLEAR_ACHIEVEMENTS = {
    1: "dragon_slayer",
    2: "frozen_conqueror",
    3: "bone_collector"
}

def check_general_achievements(player, legacy_data):
    unlocks = []
    if player.run_stats['kills'] >= 1:
        if unlock_achievement(legacy_data, "first_blood"):
            unlocks.append(ACHIEVEMENTS["first_blood"]["name"])
    if player.run_stats['boss_kills'] >= 1:
        if unlock_achievement(legacy_data, "boss_slayer"):
            unlocks.append(ACHIEVEMENTS["boss_slayer"]["name"])
    for level_required, achievement_id in LEVEL_ACHIEVEMENTS:
        if player.level >= level_required:
            if unlock_achievement(legacy_data, achievement_id):
                unlocks.append(ACHIEVEMENTS[achievement_id]["name"])
    return unlocks
