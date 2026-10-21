import streamlit as st
import json
from dungeon_rpg import (CLASS_DATA, Character, Spawn_Mob, 
    handle_victory, Spawn_Boss, save_game, load_game, get_item_by_name, shop_loot_table,
    get_unlocked_floors, create_enhanced_item)
st.title("Dungeon RPG")

def process_victory(player, mob, floor):
    rewards = handle_victory(player, mob, floor)
    st.session_state.xp_gained = rewards["xp_gained"]
    st.session_state.gold_found = rewards["gold_found"]
    if rewards["loot"]:
        st.session_state.loot_found = rewards["loot"]
    if rewards["leveled_up"]:
        st.session_state.level_message = (
            f"{player.name} reached level {player.level}!")

if "screen" not in st.session_state:
    st.session_state.screen = "char_creation"
if "player_character" in st.session_state:
    player = st.session_state.player_character
    with st.sidebar:
        st.header("Character Stats")
        st.text(player.view_stats())
        st.subheader("Equipment")
        for slot, item in player.equipment.items():
            if item:
                item_name = item.name
                if item.enhancement >0:
                    item_name += f" +{item.enhancement}"
                st.write(f"{slot}: {item_name}")
            else:
                st.write(f"{slot}: None")
                
if "combat_log" not in st.session_state:
    st.session_state.combat_log = []
if st.session_state.screen == "char_creation":
    player_name = st.text_input("Enter your character's name")

    player_class = st.selectbox("Choose a class", list(CLASS_DATA.keys()))
    stats = CLASS_DATA[player_class]

    st.write(f"HP Modifier: {stats['hp']:+}")
    st.write(f"Min Damage Modifier: {stats['min_damage']:+}")
    st.write(f"Max Damage Modifier: {stats['max_damage']:+}")
    st.write(f"Critical Chance: {stats['crit_chance']:.0%}")
    st.write(f"Ability: {stats['ability']}")
    st.write(f"Effect: {stats['ability_desc']}")
    
    st.markdown(f"*{stats['class_desc']}*")

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
    #Loading game    
    uploaded_save = st.file_uploader("Load Save File",type=["json"])
    if uploaded_save:
        save_data = load_game(uploaded_save)
        player = Character(
            save_data["name"],
            save_data["player_class"])
        saved_level = save_data["level"]
        while player.level < saved_level:
            player.level += 1
            player.min_damage += 2
            player.max_damage += 3
            player.max_hp += 10
        player.xp = save_data["xp"]
        player.gold = save_data["gold"]
        player.healing_potions = save_data["healing_potions"]
        player.highest_floor = save_data.get("highest_floor",1)
        player.signature = save_data.get("signature", None)
        player.signature_cd = save_data.get("signature_cd", 0)
        player.run_stats = save_data.get("run_stats", {"kills": 0,
            "boss_kills": 0,
            "elite_kills": 0,
            "xp_earned": 0,
            "gold_earned": 0,
            "items_found": 0
        })
        player.run_stats.setdefault("elite_kills", 0)
        for slot, item_data in save_data.get("equipment", {}).items():
            if isinstance(item_data, str):
                item = get_item_by_name(item_data)
                if item:
                    player.equip(item)
            elif item_data:
                base_item = get_item_by_name(item_data["name"])
                if base_item:
                    item = create_enhanced_item(base_item, item_data.get("enhancement", 0))
                    player.equip(item)
        for item_data in save_data.get("inventory", []):
            if isinstance(item_data, str):
                item = get_item_by_name(item_data)
                if item:
                    player.inventory.append(item)
            else:
                base_item = get_item_by_name(item_data["name"])
                if base_item:
                    item = create_enhanced_item(base_item,item_data.get("enhancement", 0))
                    player.inventory.append(item)
        player.hp = min(save_data["hp"], player.max_hp)
        st.session_state.player_character = player
        st.session_state.screen = "town"
        st.rerun()

elif st.session_state.screen == "town":
    player = st.session_state.player_character
    unlocked_floors = get_unlocked_floors(player.highest_floor)
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
        if player.level >= 10:
            if st.button("Trainer"):
                st.session_state.screen = "trainer"
                st.rerun()
        if st.button("Blacksmith"):
            st.session_state.screen = "blacksmith"
            st.rerun()

    with col2:
        with st.popover("Dungeon"):
            if len(unlocked_floors) > 1:
                selected_floor = st.radio("Choose Starting Floor", unlocked_floors,horizontal=True)
            else:
                selected_floor = 1
            if st.button("Enter Dungeon"):
                st.session_state.floor = selected_floor
                st.session_state.screen = "dungeon"
                st.rerun()
        
        save_data = save_game(player)
        if st.download_button(label="Save Game",
            data=json.dumps(save_data),
            file_name=f"{player.name}_save.json",
            mime="application/json"
            ):
                st.success("Game saved!")
        
        if st.button("Retire"):
            st.session_state.screen = "retired"
            st.rerun()
elif st.session_state.screen == "retired":
    player = st.session_state.player_character
    st.write(f"{player.name} decided to retire from adventuring.")
    stats = player.run_stats
    st.header("Career Summary")
    st.write(f"Level: {player.level}")
    st.write(f"Highest Floor Cleared: {player.highest_floor}")
    st.write(f"Monsters Defeated: {stats['kills']}")
    st.write(f"Elite Monsters Defeated: {stats['elite_kills']}")
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
        st.session_state.screen = "char_creation"
        st.rerun()            
elif st.session_state.screen == "inventory":
    player = st.session_state.player_character
    st.header("Inventory")
    st.subheader("Equipped")
    for slot, item in player.equipment.items():
        if item:
            item_name = item.name
            if item.enhancement > 0:
                item_name += f" +{item.enhancement}"
            st.write(f"{slot}: {item_name} | "
            f"HP {item.hp_bonus:+} | "
            f"Min DMG {item.min_dmg_bonus:+} | "
            f"Max DMG {item.max_dmg_bonus:+}")
        else:
            st.write(f"{slot}: None")
    st.subheader("Inventory")
    if not player.inventory:
        st.write("Your inventory is empty.")
    else:
        for i, item in enumerate(player.inventory):
            item_name = item.name
            if item.enhancement > 0:
                item_name += f" +{item.enhancement}"
            st.write(
            f"{item_name} | "
            f"HP {item.hp_bonus:+} | "
            f"Min DMG {item.min_dmg_bonus:+} | "
            f"Max DMG {item.max_dmg_bonus:+}")
            if st.button(f"Equip {item_name}", key=f"equip_{i}"):
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
    if st.button("Buy Equipment"):
        st.session_state.screen = "buy_equipment"
        st.rerun()
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
            item_name = item.name
            if item.enhancement >0:
                item_name += f" +{item.enhancement}"
            st.write(
                f"{item_name} | "
                f"HP {item.hp_bonus:+} | "
                f"Min DMG {item.min_dmg_bonus:+} | "
                f"Max DMG {item.max_dmg_bonus:+} | "
                f"Value: {item.value}g | "
                f"Sell: {item.value//2}g")
            if st.button(f"Sell {item_name}", key=f"sell_{i}"):
                player.gold += item.value//2
                sold_item = player.inventory.pop(i)
                sold_item_name = sold_item.name
                if sold_item.enhancement >0:
                    sold_item_name += f' +{sold_item.enhancement}'
                st.session_state.shop_message = (
                    f"Sold {sold_item_name} for {sold_item.value//2} gold.")
                st.rerun()
    if st.button("Return to Shop"):
        st.session_state.screen = "shop"
        st.rerun()
elif st.session_state.screen == "buy_equipment":
    if "shop_message" in st.session_state:
        st.success(st.session_state.shop_message)
        del st.session_state.shop_message
    st.header("Buy Equipment")
    for i,item in enumerate(shop_loot_table):
            st.write(
                f"{item.name} | "
                f"HP {item.hp_bonus:+} | "
                f"Min DMG {item.min_dmg_bonus:+} | "
                f"Max DMG {item.max_dmg_bonus:+} | "
                f"Value: {item.value}g | "
                )
            if st.button(f"Buy {item.name}", key=f"buy_{i}"):
                if player.gold < item.value:
                    st.error("You don't have enough gold")
                else:
                    player.gold-=item.value
                    player.inventory.append(item)
                    st.session_state.shop_message = (
                        f"Bought {item.name} for {item.value} gold.")
                    st.rerun()
    if st.button("Return to Shop"):
        st.session_state.screen = "shop"
        st.rerun()

elif st.session_state.screen == "trainer":
    st.header("Trainer")
    if "trainer_message" in st.session_state:
        st.success(st.session_state.trainer_message)
        del st.session_state.trainer_message
    st.write("I can teach you a Signature Move, for a fee. "
        "Keep in mind that you can only know one Signature Move at a time, "
        "but I can always retrain you if you'd rather learn a different one.")
    st.write(
        f"Current Signature Move: "
        f"{player.signature if player.signature else 'None'}")
    st.subheader("Reckoning - 100g")
    st.write("Deliver divine judgment upon your foe. Instantly purges Demons and Undead. Cooldown: 6 turns")
    if st.button("Learn Reckoning"):
        if player.signature == "Reckoning":
            st.error("You already know Reckoning.")
        elif player.gold >=100:
            player.gold -=100
            player.signature = "Reckoning"
            st.session_state.trainer_message = "You learned Reckoning!"
            st.rerun()
        else:
            st.error("You don't have enough gold.")
    st.subheader("Bloodlust - 125g")
    st.write("Deal double damage and restore 50% of damage dealt as HP. Cooldown: 5 turns")
    if st.button("Learn Bloodlust"):
        if player.signature == "Bloodlust":
            st.error("You already know Bloodlust.")
        elif player.gold >= 125:
            player.gold -= 125
            player.signature = "Bloodlust"
            st.session_state.trainer_message = "You learned Bloodlust!"
            st.rerun()
        else:
            st.error("You don't have enough gold.")
    st.subheader("Rejuvenation - 100g")
    st.write("Restore 70% of your maximum hp. Cooldown: 5 turns")
    if st.button("Learn Rejuvenation"):
        if player.signature == "Rejuvenation":
            st.error("You already know Rejuvenation.")
        elif player.gold >= 100:
            player.gold -= 100
            player.signature = "Rejuvenation"
            st.session_state.trainer_message = "You learned Rejuvenation!"
            st.rerun()
        else:
            st.error("You don't have enough gold.")
    if st.button("Return to Town"):
        st.session_state.screen = "town"
        st.rerun()

elif st.session_state.screen == "blacksmith":
    st.header("Blacksmith")
    if "blacksmith_message" in st.session_state:
        st.success(st.session_state.blacksmith_message)
        del st.session_state.blacksmith_message
    st.write("I can upgrade your equipment. What would you like?")
    st.write(f"Current Gold: {player.gold}g")
    st.subheader("Equipped Gear")
    equipped_items = [item for item in player.equipment.values() if item]
    if not equipped_items:
        st.write("No equipment equipped.")
    else:
        for slot, item in player.equipment.items():
            if item:
                item_name = item.name
                if item.enhancement > 0:
                    item_name += f" +{item.enhancement}"
                cost = (item.enhancement + 1) * 25
                st.write(
                    f"{slot}: {item_name} | "
                    f"HP {item.hp_bonus:+} | "
                    f"Min DMG {item.min_dmg_bonus:+} | "
                    f"Max DMG {item.max_dmg_bonus:+}")
                if item.enhancement < 50:
                    if st.button(f"Upgrade {item_name} ({cost}g)", key=f"upgrade_equipped_{slot}"):
                        if player.gold < cost:
                            st.error("You don't have enough gold.")
                        else:
                            player.gold -= cost
                            upgraded_item = create_enhanced_item(get_item_by_name(item.name),item.enhancement + 1)
                            old_name = item_name
                            new_name = upgraded_item.name
                            if upgraded_item.enhancement > 0:
                                new_name += f" +{upgraded_item.enhancement}"
                            player.equip(upgraded_item)
                            st.session_state.blacksmith_message = (f"{old_name} has been upgraded to {new_name}!")
                            st.rerun()
                else:
                    st.write("Maximum enhancement reached.")
    
    st.subheader("Inventory")
    if not player.inventory:
        st.write("Your inventory is empty.")
    else:
        for i, item in enumerate(player.inventory):
            item_name = item.name
            if item.enhancement > 0:
                item_name += f" +{item.enhancement}"
            cost = (item.enhancement + 1) * 25
            st.write(
                f"{item_name} | "
                f"HP {item.hp_bonus:+} | "
                f"Min DMG {item.min_dmg_bonus:+} | "
                f"Max DMG {item.max_dmg_bonus:+}"
            )
            if item.enhancement < 50:
                if st.button(f"Upgrade {item_name} ({cost}g)",key=f"upgrade_inventory_{i}"):
                    if player.gold < cost:
                        st.error("You don't have enough gold.")
                    else:
                        player.gold -= cost
                        upgraded_item = create_enhanced_item(get_item_by_name(item.name),item.enhancement + 1)
                        old_name = item_name
                        new_name = upgraded_item.name
                        if upgraded_item.enhancement > 0:
                            new_name += f" +{upgraded_item.enhancement}"
                        player.inventory[i] = upgraded_item
                        st.session_state.blacksmith_message = (f"{old_name} has been upgraded to {new_name}!")
                        st.rerun()
            else:
                st.write("Maximum enhancement reached.")

    if st.button("Return to Town"):
        st.session_state.screen = "town"
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
    if getattr(mob, "is_elite", False):
        st.warning(f"Elite Monster: {mob.name}!")
    if mob.hp > 0 and player.hp > 0:
        top_col1, top_col2 = st.columns(2)
        with top_col1:
            st.write(player.name)
            st.caption(f"{player.hp}/{player.max_hp}")
            st.progress(player.hp / player.max_hp)
        with top_col2:
            st.write(mob.name)
            st.caption(f"{mob.hp}/{mob.max_hp}")
            st.progress(mob.hp / mob.max_hp)
        st.subheader("Combat Log")
        if not st.session_state.combat_log:
            st.write(f"A {mob.name} appears!")
        else:
            for entry in st.session_state.combat_log[-5:]:
                st.write(entry)
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
                    process_victory(player,mob,st.session_state.floor)
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
                        process_victory(player,mob,st.session_state.floor)
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
            
            if player.signature:
                if st.button(f"{player.signature} (CD: {player.signature_cd})"):
                    result = player.use_signature(mob)
                    if result is None:
                        st.error(f"{player.signature} is on cooldown: {player.signature_cd} turns remaining.")
                    else:
                        if result['damage'] > 0:
                            st.session_state.combat_log.append(f"You dealt {result['damage']} damage using {player.signature}!")
                        if result['heal'] > 0:
                            st.session_state.combat_log.append(f"You healed {result['heal']} HP using {player.signature}!")
                        if result['instakill']:
                            st.session_state.combat_log.append(f"{player.signature} destroyed the {mob.name}!")
                        if mob.hp  <= 0:
                            st.session_state.combat_log.append(f"You defeated the {mob.name}.")
                            process_victory(player,mob,st.session_state.floor)
                        else:
                            base_damage = mob.attack()
                            enemy_damage = mob.use_ability(base_damage)
                            if enemy_damage is None:
                                enemy_damage = base_damage
                                st.session_state.combat_log.append(f"The {mob.name} hit you for {enemy_damage} damage.")
                                mob.reduce_cooldown()
                            else:
                                st.session_state.combat_log.append(
                                    f"The {mob.name} used {mob.ability_name}! It dealt {enemy_damage} damage.")
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
        player.highest_floor = max(player.highest_floor, st.session_state.floor)
        if st.session_state.floor % 5 == 0:
            st.success("Boss Defeated!")
        st.write(f"You gained {st.session_state.xp_gained} XP.")
        st.write(f"You found {st.session_state.gold_found} gold.")
        if "loot_found" in st.session_state:
            loot = st.session_state.loot_found
            if loot == "Healing potion":
                st.write(f"The {mob.name} dropped a Healing Potion!")
            else:
                loot_name = loot.name
                if loot.enhancement>0:
                    loot_name += f' +{loot.enhancement}'
                st.write(f"The {mob.name} dropped a {loot_name}!")
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
        stats = player.run_stats
        st.header("Life Summary")
        st.write(f"Level: {player.level}")
        st.write(f"Highest Floor Cleared: {player.highest_floor}")
        st.write(f"Monsters Defeated: {stats['kills']}")
        st.write(f"Elite Monsters Defeated: {stats['elite_kills']}")
        st.write(f"Bosses Defeated: {stats['boss_kills']}")
        st.write(f"XP Earned: {stats['xp_earned']}")
        st.write(f"Gold Earned: {stats['gold_earned']}")
        st.write(f"Items Found: {stats['items_found']}")
        if st.button("Game Over"):
            st.session_state.combat_log = []
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
