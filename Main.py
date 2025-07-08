
# Wobbling Wally Wrecks Welland

# ver 0/01 #added colorama so game could be compiled into a Windows executable file

print("Wobbling Wally Wrecks Welland\n\n")

# Import Colorama and initialize it
from colorama import Fore, Style, init
init() # Initialize Colorama for Windows compatibility.

COLOUR_CYAN = Fore.CYAN
COLOUR_RESET = Style.RESET_ALL
COLOUR_RED = Fore.RED          # Bright Red (for monster attack messages)
COLOUR_GREEN = Fore.GREEN      # Successful attack

from help import help
from help import map
from Character import Character
from Move import LOCATIONS
from Move import MAP_CONNECTIONS
import random
import time
current_location_id = 1


Wally = Character(-5, 1, "pudding sharp intellect", 4, 2,True)

NORTH = "n"
EAST = "e"
SOUTH = "s"
WEST = "w"


def monster_attacks(monster_data, player_char):
    """
    Handles a monster's attack on the player with random damage between 1 and its strength.
    If player is defeated, they respawn at the start location with full HP.
    Returns True if player respawned (meaning the game continues), False if no respawn.
    """
    print(
        f"\n{COLOUR_RED}The {monster_data['type']} suddenly attacks you with {monster_data['weapon']}!{COLOUR_RESET}")

    # --- NEW DAMAGE CALCULATION ---
    # Damage is now a random value between 1 and the monster's full strength.
    # If strength is 0 or less, damage will be 0 (a special "too weak" case).
    if monster_data['strength'] <= 0:
        damage = 0
        print(f"The {monster_data['type']} tries to hit you...")
        time.sleep(1)
        print(" but it's too weak to cause any damage!")
    else:
        # Note: As per your provided code, damage is 1 to HALF of monster's strength here.
        # If you meant to use full strength, remove the '// 2'.
        damage = random.randint(1, monster_data['strength'] // 2)

    # Apply damage only if it's greater than 0
    if damage > 0:
        player_char.hitpoints -= damage
        time.sleep(1)
        print(f"You take {damage} damage! You now have {player_char.hitpoints} out of {player_char.max_hitpoints} hitpoints.")
    # The 'else' case (damage is 0) is already handled by the "too weak" print above, so no new print here.

    if player_char.hitpoints <= 0:
        # --- WALLY IS DEFEATED - INITIATE RESPAWN ---
        player_char.hitpoints = player_char.max_hitpoints  # Restore HP to full
        player_char.is_alive = True  # Wally is revived and ready to go!

        global current_location_id
        current_location_id = 1  # Send Wally back to the starting location (Hooker Street)

        print(f"\n{COLOUR_RED}The {monster_data['type']} blams you all the way back to Hooker Street.{COLOUR_RESET}")
        print(f"{COLOUR_RED}Wally: 'I should have just stayed here.'{COLOUR_RESET}")
        print(f"You find yourself back at Hooker Street, feeling refreshed ({player_char.hitpoints} HP).")

        return True  # Indicate that Wally "died" and respawned (game continues)
    else: # <-- This else block ensures a return False if Wally survives
        return False # Indicate that Wally is still alive after the attack (game continues normally)


# --- Main Game Loop ---
def run_perpetually():
    global current_location_id
    global Wally

    while True:
        current_room_data = LOCATIONS[current_location_id]
        print(f"\n--- You are now in: {current_room_data['description']} ---")

        monster_in_room = current_room_data.get("monster")
        monster_is_alive = False
        if monster_in_room and monster_in_room["is_alive"]:
            monster_is_alive = True
            print(f"  A{monster_in_room['type']} is eyeing you. It is armed with {monster_in_room['weapon']}.")
            if monster_in_room['hitpoints'] < monster_in_room['max_hitpoints']:
                print(f"  It has {monster_in_room['hitpoints']} HP remaining.")
        elif monster_in_room:
            print(f"The husk of a {monster_in_room['type']} lies defeated here.")

        user_move = input(f"{COLOUR_CYAN}wut do? {COLOUR_RESET}").lower()

        # --- Combat Actions (Fight) ---
        if monster_is_alive and user_move == "f":  # Player chooses to Fight a living monster
            print(f"{COLOUR_GREEN}You prepare to attack the {monster_in_room['type']}!{COLOUR_RESET}")

            wally_damage = Wally.attack()
            monster_in_room['hitpoints'] -= wally_damage
            time.sleep(1)

            print(f"You strike the {monster_in_room['type']} with your {Wally.weapon} for {wally_damage} damage!")

            if monster_in_room['hitpoints'] <= 0:
                monster_in_room['is_alive'] = False
                print(
                    f"{COLOUR_GREEN}The {monster_in_room['type']} lets out a pathetic squeal and falls defeated!{COLOUR_RESET}")
            else:
                print(f"The {monster_in_room['type']} has {monster_in_room['hitpoints']} HP left.")
                # Monster's Turn to Attack (if it's still alive)
                respawn_occurred = monster_attacks(monster_in_room, Wally)
                if respawn_occurred:
                    continue  # If Wally respawned, restart the loop

            continue  # Restart the loop after a combat turn

        # --- Movement Actions (Now a True Flee Attempt) ---
        elif user_move in [NORTH, SOUTH, EAST, WEST]:
            possible_exits = MAP_CONNECTIONS.get(current_location_id, {})

            if user_move in possible_exits:
                # Store current HP before healing to check if healing actually occurred
                old_wally_hp = Wally.hitpoints
                # VALID MOVE: Successfully flee and move to the new room
                current_location_id = possible_exits[user_move]

                # Always restore HP when successfully changing rooms (flee or otherwise)
                Wally.hitpoints = Wally.max_hitpoints

                if Wally.hitpoints > old_wally_hp:
                    print(
                        f"\nYou move {user_move.upper()}. You feel refreshed.")
                else:
                    # If HP was already max, just print the move message
                    print(f"\nYou move {user_move.upper()}.")

                # If there was a monster, tell the player they successfully fled
                if monster_is_alive:
                    print(f"You successfully slipped away from a{monster_in_room['type']}!")

                continue  # Restart the loop to display the new room (no monster attack on successful flee)

            else:
                # INVALID MOVE: Can't go that way
                print("You can't go that way from here.")

                # If there was a monster, it attacks because you failed to move
                if monster_is_alive:
                    print(
                        f"{COLOUR_RED}You try to escape, but the {monster_in_room['type']} blocks your path and attacks!{COLOUR_RESET}")
                    respawn_occurred = monster_attacks(monster_in_room, Wally)
                    if respawn_occurred:
                        continue  # If Wally respawned, restart the loop

        # --- Handle all other commands (non-movement or invalid moves that provoke attack) ---
        else:
            if monster_is_alive:
                respawn_occurred = monster_attacks(monster_in_room, Wally)
                if respawn_occurred:
                    continue

            if user_move == "?":
                # FIXED TYPO: changed '.in' to '.join'
                print("\n" + ", ".join(help))
            elif user_move == "m":
                print("\n--- Map ---")
                for line in map:
                    print(line)
            elif user_move == "i":
                print(f"\nYou are armed with {Wally.weapon}.")
            elif user_move == "c":
                print(f"\n--- Character Stats ---")
                print(f"Wally's strength is {Wally.strength}")
                print(f"Wally's speed is {Wally.speed}")
                print(f"Wally's weapon is {Wally.weapon}")
                print(f"Wally's hitpoints are {Wally.hitpoints}")
                print(f"Wally's xp is {Wally.xp}")
                print(f"You are still alive: {Wally.is_alive}")
            elif user_move == "l":
                print(f"\n--- Look Around ---")
                print(current_room_data['description'])
                if monster_in_room:
                    if monster_in_room["is_alive"]:
                        print(
                            f"  A {monster_in_room['type']} is eyeing you. They are armed with {monster_in_room['weapon']}.")
                        if monster_in_room['hitpoints'] < monster_in_room['max_hitpoints']:
                            print(f"  It has {monster_in_room['hitpoints']} HP remaining.")
                    else:
                        print(f"The husk of a {monster_in_room['type']} lies defeated here.")
            elif user_move == "x":
                print("\nYou scairt, bruh? Game Over!")
                break
            else:
                print("Get some help! (?)")


run_perpetually()