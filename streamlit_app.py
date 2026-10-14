import streamlit as st
import random
from dungeon_rpg import CLASS_DATA, Character, Spawn_Mob, Item, Loot_Drop, handle_victory, Spawn_Boss
st.title("Dungeon RPG")

if "screen" not in st.session_state:
    st.session_state.screen = "char_creation"
if "player_character" in st.session_state:
    player = st.session_state.player_character
    with st.sidebar:
        st.header("Character Stats")
        st.text(player.view_stats())
if "combat_log" not in st.session_state:
    st.session_state.combat_log = []
if st.session_state.screen == "char_creation":
    player_name = st.text_input("Enter your character's name")

    player_class = st.selectbox("Choose a class", list(CLASS_DATA.keys()))
    stats = CLASS_DATA[player_class]

    st.write(f"HP Modifier: {stats['hp']:+}")
    st.write(f"Min Damage Modifier: {stats['min_damage']:+}")
    st.write(f"Max Damage Modifier: {stats['max_damage']:+}")
    st.write(f"Ability: {stats['ability']}")
    st.write(f"Effect: {stats['ability_desc']}")

    if st.button("Create Character"):
        name = player_name.strip()
        if not name:
            st.error("Please enter a name.")
        elif len(name) > 15:
            st.error("Names must be 15 characters or fewer.")
        else:
            st.session_state.player_character = Character(
                name.title(),
                player_class
            )
            st.session_state.screen = "town"
            st.rerun()

elif st.session_state.screen == "town":
    player = st.session_state.player_character
    if "run_stats" not in st.session_state:
        st.session_state.run_stats = {
            "kills": 0,
            "boss_kills": 0,
            "xp_earned": 0,
            "gold_earned": 0,
            "items_found": 0}
    st.header("Town")
    if "inn_message" in st.session_state:
        st.success(st.session_state.inn_message)
        del st.session_state.inn_message
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Shop"):
            st.session_state.screen = "shop"
            st.rerun()
        if st.button("Inn (5g)"):
            if player.gold < 5:
                st.error("Not enough gold!")
            else:
                player.hp = player.max_hp
                st.session_state.inn_message = (f"You rested at the inn and recovered to full health. HP: {player.hp}/{player.max_hp}.")
                player.gold -= 5
                st.rerun()
        if st.button("Inventory"):
            st.session_state.screen = "inventory"
            st.rerun()

    with col2:
        if st.button("Dungeon"):
            st.session_state.screen = "dungeon"
            st.rerun()
        if st.button("Retire"):
            st.session_state.screen = "retired"
            st.rerun()
elif st.session_state.screen == "retired":
    player = st.session_state.player_character
    st.write(f"{player.name} decided to retire from adventuring.")
    stats = st.session_state.run_stats
    st.header("Career Summary")
    st.write(f"Level: {player.level}")
    st.write(f"Monsters Defeated: {stats['kills']}")
    st.write(f"Bosses Defeated: {stats['boss_kills']}")
    st.write(f"XP Earned: {stats['xp_earned']}")
    st.write(f"Gold Earned: {stats['gold_earned']}")
    st.write(f"Items Found: {stats['items_found']}")
    if st.button("Game over"):
        del st.session_state.player_character
        if "mob" in st.session_state:
            del st.session_state.mob
        if "level_message" in st.session_state:
            del st.session_state.level_message
        if "gold_found" in st.session_state:
            del st.session_state.gold_found
        if "loot_found" in st.session_state:
            del st.session_state.loot_found
        if "xp_gained" in st.session_state:
            del st.session_state.xp_gained
        if "floor" in st.session_state:
            del st.session_state.floor
        if "run_stats" in st.session_state:
            del st.session_state.run_stats
        st.session_state.screen = "char_creation"
        st.rerun()            
elif st.session_state.screen == "inventory":
    player = st.session_state.player_character
    st.header("Inventory")
    st.subheader("Equipped")
    for slot, item in player.equipment.items():
        if item:
            st.write(f"{slot}: {item.name} | "
            f"HP +{item.hp_bonus} | "
            f"Min DMG +{item.min_dmg_bonus} | "
            f"Max DMG +{item.max_dmg_bonus}")
        else:
            st.write(f"{slot}: None")
    st.subheader("Inventory")
    if not player.inventory:
        st.write("Your inventory is empty.")
    else:
        for i, item in enumerate(player.inventory):
            st.write(
            f"{item.name} | "
            f"HP +{item.hp_bonus} | "
            f"Min DMG +{item.min_dmg_bonus} | "
            f"Max DMG +{item.max_dmg_bonus}")
            if st.button(f"Equip {item.name}", key=f"equip_{i}"):
                old_item = player.equipment[item.slot]
                player.equip(item)
                if old_item:
                    player.inventory.append(old_item)
                player.inventory.pop(i)
                st.rerun()

    if st.button("Return to Town"):
        st.session_state.screen = "town"
        st.rerun()

elif st.session_state.screen == "shop":
    player = st.session_state.player_character
    st.header("Shop")
    if "shop_message" in st.session_state:
        st.success(st.session_state.shop_message)
        del st.session_state.shop_message
    if st.button("Buy Potion (5g)"):
        if player.gold >= 5:
            player.gold -= 5
            player.healing_potions += 1
            st.session_state.shop_message = (f"Potion purchased for 5g. You now have {player.healing_potions} potions.")
            st.rerun()
        else:
            st.error("Not enough gold!")
    if st.button("Sell"):
        st.session_state.screen = "sell"
        st.rerun()
    if st.button("Leave"):
        st.session_state.screen = "town"
        st.rerun()

elif st.session_state.screen == "sell":
    player = st.session_state.player_character
    if "shop_message" in st.session_state:
        st.success(st.session_state.shop_message)
        del st.session_state.shop_message
    st.header("Sell Items")
    if not player.inventory:
        st.write("You have nothing to sell")
    else:
        for i,item in enumerate(player.inventory):
            st.write(
                f"{item.name} | "
                f"HP +{item.hp_bonus} | "
                f"Min DMG +{item.min_dmg_bonus} | "
                f"Max DMG +{item.max_dmg_bonus} | "
                f"Value: {item.value}g | "
                f"Sell: {item.value//2}g")
            if st.button(f"Sell {item.name}", key=f"sell_{i}"):
                player.gold += item.value//2
                sold_item = player.inventory.pop(i)
                st.session_state.shop_message = (
                    f"Sold {sold_item.name} for {sold_item.value//2} gold.")
                st.rerun()
    if st.button("Return to Shop"):
        st.session_state.screen = "shop"
        st.rerun()

elif st.session_state.screen == "dungeon":
    player = st.session_state.player_character
    if "floor" not in st.session_state:
        st.session_state.floor = 1
    st.header(f"Dungeon - Floor: {st.session_state.floor}")
    if st.session_state.floor % 5 == 0:
        st.warning("Boss Floor!")
    if "mob" not in st.session_state:
        if st.session_state.floor % 5 ==0:
            st.session_state.mob = Spawn_Boss(st.session_state.floor)
        else:
            st.session_state.mob = Spawn_Mob(st.session_state.floor)
    mob = st.session_state.mob
    st.subheader("Combat Log")
    if not st.session_state.combat_log:
        st.write(f"A {mob.name} appears!")
    else:
        for entry in st.session_state.combat_log[-2:]:
            st.write(entry)
    if mob.hp > 0 and player.hp > 0:
        st.write(f"{mob.name} HP: {max(0, mob.hp)}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Attack"):
                damage, crit = player.attack()
                player.reduce_cooldown()
                mob.hp -= damage
                if crit:
                    st.session_state.combat_log.append(f"Critical hit! You hit the {mob.name} for {damage} damage.")
                else:
                    st.session_state.combat_log.append(f"You hit the {mob.name} for {damage} damage.")
                if mob.hp <= 0:
                    st.session_state.combat_log.append(f"You defeated the {mob.name}.")
                    rewards = handle_victory(player, mob, st.session_state.floor)
                    st.session_state.run_stats["kills"] +=1 
                    if st.session_state.floor % 5 == 0:
                        st.session_state.run_stats["boss_kills"] +=1    
                    st.session_state.run_stats["xp_earned"] += rewards["xp_gained"]
                    st.session_state.run_stats["gold_earned"] += rewards["gold_found"]
                    st.session_state.xp_gained = rewards["xp_gained"]
                    st.session_state.gold_found = rewards["gold_found"]
                    if rewards["loot"]:
                        st.session_state.loot_found = rewards["loot"]
                        st.session_state.run_stats["items_found"] += 1
                    if rewards["leveled_up"]:
                        st.session_state.level_message = (f"{player.name} reached level {player.level}!")
                else:
                    base_damage = mob.attack()
                    enemy_damage = mob.use_ability(base_damage)
                    if enemy_damage is None:
                        enemy_damage = base_damage
                        st.session_state.combat_log.append(f"The {mob.name} hit you for {enemy_damage} damage.")
                        mob.reduce_cooldown()
                    else:
                        st.session_state.combat_log.append(f"The {mob.name} used {mob.ability_name}! It dealt {enemy_damage} damage.")
                    player.hp -= enemy_damage
                st.rerun()
            
            if st.button(f"{player.special_ability} (CD: {player.special_cooldown})"):
                result = player.use_special(mob)
                if result is None:
                    st.error(f"{player.special_ability} is on cooldown: {player.special_cooldown} turns remaining.")
                else:
                    damage, crit = result
                    if crit:
                        st.session_state.combat_log.append(f"Critical hit! Your {player.special_ability} did {damage} damage.")
                    else:
                        st.session_state.combat_log.append(f"Your {player.special_ability} did {damage} damage.")
                    if mob.hp <= 0:
                        st.session_state.combat_log.append(f"You defeated the {mob.name}.")
                        rewards = handle_victory(player, mob, st.session_state.floor)
                        st.session_state.run_stats["kills"] +=1 
                        if st.session_state.floor % 5 == 0:
                            st.session_state.run_stats["boss_kills"] +=1    
                        st.session_state.run_stats["xp_earned"] += rewards["xp_gained"]
                        st.session_state.run_stats["gold_earned"] += rewards["gold_found"]
                        st.session_state.xp_gained = rewards["xp_gained"]
                        st.session_state.gold_found = rewards["gold_found"]
                        if rewards["loot"]:
                            st.session_state.loot_found = rewards["loot"]
                            st.session_state.run_stats["items_found"] += 1
                        if rewards["leveled_up"]:
                            st.session_state.level_message = (f"{player.name} reached level {player.level}!")
                    else:
                        base_damage = mob.attack()
                        enemy_damage = mob.use_ability(base_damage)
                        if enemy_damage is None:
                            enemy_damage = base_damage
                            st.session_state.combat_log.append(f"The {mob.name} hit you for {enemy_damage} damage.")
                            mob.reduce_cooldown()
                        else:
                            st.session_state.combat_log.append(f"The {mob.name} used {mob.ability_name}! It dealt {enemy_damage} damage.")
                        player.hp -= enemy_damage
                    st.rerun()

        with col2:
            if st.button("Use Potion"):
                if player.healing_potions > 0:
                    healed = player.use_potion()
                    player.reduce_cooldown()
                    st.session_state.combat_log.append(f"You regained {healed} HP.")
                    if mob.hp > 0:
                        base_damage = mob.attack()
                        enemy_damage = mob.use_ability(base_damage)
                        if enemy_damage is None:
                            enemy_damage = base_damage
                            st.session_state.combat_log.append(f"The {mob.name} hit you for {enemy_damage} damage.")
                            mob.reduce_cooldown()
                        else:
                            st.session_state.combat_log.append(f"The {mob.name} used {mob.ability_name}! It dealt {enemy_damage} damage.")
                    player.hp -= enemy_damage
                    st.rerun()
                else:
                    st.error("You have no potions!")

    elif mob.hp <=0 and player.hp > 0:
        st.subheader("Victory!")
        if st.session_state.floor % 5 == 0:
            st.success("Boss Defeated!")
        st.write(f"You gained {st.session_state.xp_gained} XP.")
        st.write(f"You found {st.session_state.gold_found} gold.")
        if "loot_found" in st.session_state:
            loot = st.session_state.loot_found
            if loot == "Healing potion":
                st.write(f"The {mob.name} dropped a Healing Potion!")
            else:
                st.write(f"The {mob.name} dropped a {loot.name}!")
        if "level_message" in st.session_state:
            st.success(st.session_state.level_message)
        if st.button("Continue"):
            st.session_state.floor += 1
            st.session_state.combat_log = []
            if "level_message" in st.session_state:
                del st.session_state.level_message
            if "gold_found" in st.session_state:
                del st.session_state.gold_found
            if "loot_found" in st.session_state:
                del st.session_state.loot_found
            del st.session_state.mob
            if "xp_gained" in st.session_state:
                del st.session_state.xp_gained
            st.rerun()
            
        if st.button("Return to Town"):
            st.session_state.combat_log = []
            if "level_message" in st.session_state:
                del st.session_state.level_message
            if "gold_found" in st.session_state:
                del st.session_state.gold_found
            if "loot_found" in st.session_state:
                del st.session_state.loot_found
            del st.session_state.mob
            if "xp_gained" in st.session_state:
                del st.session_state.xp_gained
            st.session_state.floor = 1
            st.session_state.screen = "town"
            st.rerun()
    
    else:
        st.error("You died!")
        stats = st.session_state.run_stats
        st.header("Life Summary")
        st.write(f"Level: {player.level}")
        st.write(f"Monsters Defeated: {stats['kills']}")
        st.write(f"Bosses Defeated: {stats['boss_kills']}")
        st.write(f"XP Earned: {stats['xp_earned']}")
        st.write(f"Gold Earned: {stats['gold_earned']}")
        st.write(f"Items Found: {stats['items_found']}")
        if st.button("Game Over"):
            st.session_state.combat_log = []
            if "run_stats" in st.session_state:
                del st.session_state.run_stats
            del st.session_state.player_character
            if "mob" in st.session_state:
                del st.session_state.mob
            if "level_message" in st.session_state:
                del st.session_state.level_message
            if "gold_found" in st.session_state:
                del st.session_state.gold_found
            if "loot_found" in st.session_state:
                del st.session_state.loot_found
            if "xp_gained" in st.session_state:
                del st.session_state.xp_gained
            st.session_state.floor = 1
            st.session_state.screen = "char_creation"
            st.rerun()