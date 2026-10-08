import streamlit as st
from dungeon_rpg import CLASS_DATA, Character, Spawn_Mob
st.title("Dungeon RPG")

if "screen" not in st.session_state:
    st.session_state.screen = "char_creation"
if "player_character" in st.session_state:
    player = st.session_state.player_character
    with st.sidebar:
        st.header("Character Stats")
        st.text(player.view_stats())
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
    st.header("Town")
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
                player.gold -= 5
                st.rerun()

    with col2:
        if st.button("Dungeon"):
            st.session_state.screen = "dungeon"
            st.rerun()
        if st.button("Retire"):
            del st.session_state.player_character
            if "mob" in st.session_state:
                del st.session_state.mob

            if "level_message" in st.session_state:
                del st.session_state.level_message
            st.session_state.screen = "char_creation"
            st.rerun()



elif st.session_state.screen == "shop":
    player = st.session_state.player_character
    st.header("Shop")
    if st.button("Buy Potion (5g)"):
        if player.gold >= 5:
            player.gold -= 5
            player.healing_potions += 1
            st.success("Potion purchased!")
            st.rerun()
        else:
            st.error("Not enough gold!")
    if st.button("Sell"):
        st.write("Coming Soon")
    if st.button("Leave"):
        st.session_state.screen = "town"
        st.rerun()

    
elif st.session_state.screen == "dungeon":
    player = st.session_state.player_character
    st.header("Dungeon")
    if "mob" not in st.session_state:
        st.session_state.mob = Spawn_Mob(1)
    mob = st.session_state.mob
    st.write(f"A {mob.name} appears!")
    if mob.hp > 0 and player.hp > 0:
        st.write(f"HP: {max(0,mob.hp)}")
        if st.button("Attack"):
            damage = player.attack()
            mob.hp -= damage
            if mob.hp <= 0:
                player.xp += mob.xp_reward
                leveled_up = player.level_up()
                if leveled_up:
                    st.session_state.level_message = (f"{player.name} reached level {player.level}")
            else:
                player.hp -= mob.attack()
            st.rerun()

    elif mob.hp <=0 and player.hp > 0:
        st.success(f"You defeated the {mob.name}!")
        st.write(f"You gained {mob.xp_reward} XP!")
        if "level_message" in st.session_state:
            st.success(st.session_state.level_message)
        if st.button("Return to Town"):
            if "level_message" in st.session_state:
                del st.session_state.level_message
            del st.session_state.mob
            st.session_state.screen = "town"
            st.rerun()
    
    else:
        st.error("You died!")
        if st.button("Game Over"):
            del st.session_state.player_character
            del st.session_state.mob
            if "level_message" in st.session_state:
                del st.session_state.level_message
            st.session_state.screen = "char_creation"
            st.rerun()