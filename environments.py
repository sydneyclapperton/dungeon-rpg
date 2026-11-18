#Functions
def necrotic_aura(player, floor):
    damage = floor
    player.hp = max(0, player.hp - damage)
    return(f"Necrotic Aura dealt {damage} damage to you.")

def run_end_of_turn(environment, player, floor):
    effect = environment["end_of_turn"]
    if effect:
        return effect(player, floor)
    return None


ENVIRONMENTS = {
    "none": {
        "name": "Ancient Silence",
        "description": "No environmental effects.",
        "healing_modifier": 1.0,
        "enemy_damage_modifier": 1.0,
        "player_damage_modifier": 1.0,
        "start_of_turn": None,
        "end_of_turn": None,
        "on_combat_start": None,
        "on_combat_end": None
    },
    "bitter_cold": {
        "name": "Bitter Cold",
        "description": "Healing effects are reduced by 25%.",
        "healing_modifier": 0.75,
        "enemy_damage_modifier": 1.0,
        "player_damage_modifier": 1.0,
        "start_of_turn": None,
        "end_of_turn": None,
        "on_combat_start": None,
        "on_combat_end": None
    },
    "necrotic_aura": {
        "name": "Necrotic Aura",
        "description": (
            "Living creatures suffer necrotic damage equal "
            "to the current floor at the end of each turn."
        ),
        "healing_modifier": 1.0,
        "enemy_damage_modifier": 1.0,
        "player_damage_modifier": 1.0,
        "start_of_turn": None,
        "end_of_turn": necrotic_aura,
        "on_combat_start": None,
        "on_combat_end": None
    }
}
