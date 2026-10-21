import streamlit as st
import random
from dungeon_rpg import enhance_item, basic_loot_table, create_enhanced_item

event_pool =[
  "treasure",
  "healing_fountain",
  "shrine",
  "trap"
  ]
def trigger_event(player, floor):
  event = random.choice(event_pool)
  if event == 'treasure':
    return {"type":"treasure", "title": "Treasure Chest", "message":"You found a treasure chest!"}
  elif event =="trap":
    return {"type":"trap", "title": "Trap", "message":"You triggered a trap!"}
  elif event =="healing_fountain":
    return {"type":"healing_fountain", "title":"Healing Fountain", "message":"You found a healing fountain!"}
  elif event == "shrine":
    return {"type":"shrine", "title":"Shrine", "message": "You found a shrine!"}
  else:
    return {"type": "unknown", "title": "Nothing Happens","message": "The dungeon is eerily quiet."}

def treasure_event(player,floor):
  if "event_result" not in st.session_state:
    if st.button("Open Chest"):
      reward = random.random()
      if reward < 0.05:
        damage = floor*2 + 10
        player.hp = max(1, player.hp - damage)
        st.session_state.event_result =(f"It was a trap! You take {damage} damage.")
      elif reward < 0.5:
          gold = random.randint(floor * 2,floor * 5)
          player.gold += gold
          st.session_state.event_result = (f"You found {gold} gold!")
      elif reward < 0.8:
          player.healing_potions += 1
          st.session_state.event_result = ("You found a Healing Potion!")
      else:
          item = enhance_item(random.choice(basic_loot_table),floor)
          player.inventory.append(item)
          item_name = item.name
          if item.enhancement > 0:
              item_name += f" +{item.enhancement}"
          st.session_state.event_result = (f"You found {item_name}!")
      st.rerun()
    if st.button("Leave Chest"):
      st.session_state.event_result = ("You decide not to risk opening the chest.")
      st.rerun()

def healing_fountain_event(player):
    if "event_result" not in st.session_state:
        if st.button("Drink"):
            heal = player.max_hp // 2
            player.hp = min(player.max_hp, player.hp + heal)
            st.session_state.event_result = (f"You recover {heal} HP.")
            st.rerun()
        if st.button("Leave"):
            st.session_state.event_result = ("You leave the fountain untouched.")
            st.rerun()

def shrine_event(player, floor):
    if "event_result" not in st.session_state:
        st.write("Choose a blessing from the shrine.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Gain Gold"):
                gold = random.randint(floor * 5, floor * 10)
                player.gold += gold
                st.session_state.event_result = (f"The shrine blesses you with {gold} gold.")
                st.rerun()
            if st.button("Gain XP"):
                xp = floor * 5
                player.xp += xp
                player.run_stats["xp_earned"] += xp
                leveled_up = player.level_up()
                if leveled_up:
                    st.session_state.event_result = (f"The shrine grants {xp} XP. You leveled up!")
                else:
                    st.session_state.event_result = (f"The shrine grants {xp} XP.")
                st.rerun()

        with col2:
            if st.button("Restore Health"):
                heal_amount = player.max_hp - player.hp
                player.hp = player.max_hp
                st.session_state.event_result = (f"The shrine restores {heal_amount} HP.")
                st.rerun()
            if st.button("Enhance Equipment"):
                equipped_slots = [slot for slot, item in player.equipment.items()if item]
                if equipped_slots:
                    slot = random.choice(equipped_slots)
                    current_item = player.equipment[slot]
                    player.equipment[slot] = create_enhanced_item(current_item,current_item.enhancement + 1)
                    upgraded_item = player.equipment[slot]
                    st.session_state.event_result = (f"The shrine enhances {upgraded_item.name} to +{upgraded_item.enhancement}!")
                    st.rerun()
                else:
                    st.session_state.event_result = ("You have no equipment for the shrine to bless.")
                    st.rerun()
    else:
        st.success(st.session_state.event_result)

def trap_event(player, floor):
    if "event_result" not in st.session_state:
        if player.player_class == "Rogue":
            st.session_state.event_result = ("Your rogue instincts detect a nearly invisible tripwire. You effortlessly avoid the trap.")
            st.rerun()
        st.write("A hidden trap springs!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Try to Dodge"):
                if random.random() < 0.35:
                    st.session_state.event_result = ("You dive out of the way and avoid the trap!")
                else:
                    damage = floor * 2 + 10
                    player.hp = max(1, player.hp - damage)
                    st.session_state.event_result = (f"You fail to dodge and take {damage} damage!")
                st.rerun()
        with col2:
            if st.button("Brace Yourself"):
                damage = (floor * 2 + 10) // 2
                player.hp = max(1, player.hp - damage)
                st.session_state.event_result = (f"You brace for impact and take only {damage} damage.")
                st.rerun()

    else:
        st.success(st.session_state.event_result)