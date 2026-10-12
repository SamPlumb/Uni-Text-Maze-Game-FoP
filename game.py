"""
Keyerror: The Keeper of the Golden Key
game.py

Core game loop:
connects the menus, prompts and logic modules to run the game.
"""

import leaderboard
import logic
import menus
from ui import d_box


def main_menu_loop() -> dict:
    """
    Run the main menu until the player starts a game, and return the new game state.
    Prompts the player to choose from the main menu options:
    new game, leaderboard, remove leaderboard entry, or exit the game.
    """
    while True:
        menus.main_menu()
        choice = menus.prompt_choice(4)

        if choice == 1:
            state = logic.new_game()
            menus.game_intro()
            return state

        if choice == 2:
            menus.display_leaderboard(leaderboard.load())

        elif choice == 3:
            remove_leaderboard_entry()

        else:
            logic.exit_game()


def remove_leaderboard_entry() -> None:
    """
    Remove a leaderboard entry.
    """
    entries = leaderboard.load()

    if not entries:
        menus.display_leaderboard(entries)
        return

    menus.remove_leaderboard_entry_menu(entries)
    choice = menus.prompt_choice(len(entries) + 1)

    if choice == len(entries) + 1:  # Return to the main menu
        return

    if leaderboard.remove_score(entries[choice - 1]):
        d_box(["The leaderboard entry has been removed from the leaderboard."])
    else:
        d_box(["That entry could not be found in the leaderboard."])


def record_win(state: dict) -> None:
    """
    Show the win screen and save the player's time under the name they enter.
    """
    seconds = logic.game_timer(state)
    menus.you_win_menu(seconds)

    while True:
        name = input().strip()

        if name:
            break

        d_box(["Player name cannot be empty. Please enter a valid name."])

    try:
        leaderboard.add_score(name, seconds)
    except OSError as error:
        d_box([f"Could not save score: {error}"])


def move_room(state: dict) -> None:
    """
    Show the move room menu and update the game state based on the player's choice.
    """
    menus.move_room_menu(state["room"])
    exits = logic.current_room_exits(state["room"])
    choice = menus.prompt_choice(len(exits) + 1)

    if choice == len(exits) + 1:  # choose to not move, return to the game menu
        return

    old_room = state["room"]
    logic.move_player_room(state, exits[choice - 1][1])
    d_box([f"You have left the {old_room} and entered the {state['room']}."])


def explore_room(state: dict) -> None:
    """
    Show the explore room menu and update the game state based on the player's choice.
    """
    objects = state["room_objects"][state["room"]]
    menus.explore_room_menu(state["room"], objects)

    choice = menus.prompt_choice(len(objects) + 1)

    if choice == len(objects) + 1:  # choose to not investigate any object, return to the game menu
        return

    index = choice - 1
    item = state["room_items"][state["room"]][index]
    menus.investigate_object_menu(objects[index], item)
    logic.pick_up_item(state, index)


def use_item(state: dict, usable_items: list[str]) -> bool:
    """
    Show the use item menu and update the game state based on the player's choice.
    Returns True if the player wins the game, False otherwise.
    """
    menus.use_item_menu(usable_items)
    choice = menus.prompt_choice(len(usable_items) + 1)

    if choice == len(usable_items) + 1:  # No item to use, return to game menu
        return False

    outcome = logic.use_item(state, usable_items[choice - 1])

    if outcome == logic.use_map:
        menus.open_map()
    elif outcome == logic.use_no_lock:
        d_box(["You try to use the Golden Key, but it doesn't fit any lock in this room."])
    elif outcome == logic.use_invalid:
        d_box(["You cannot use that item."])

    return outcome == logic.use_win


def craft_item(state: dict, craftable_items: list[str]) -> None:
    """
    Show the crafting menu and update the game state based on the player's choice.
    """
    menus.crafting_menu(craftable_items)
    choice = menus.prompt_choice(len(craftable_items) + 1)

    if choice == len(craftable_items) + 1:  # choose to not craft any item, return to the game menu
        return

    item = craftable_items[choice - 1]

    if logic.craft_item(state["pockets"], item):
        d_box([f"You have successfully crafted a {item}."])
    else:
        d_box([f"You do not have the necessary ingredients to craft a {item}."])


def play_turn(state: dict) -> bool:
    """
    Show the game menu and update the game state based on the player's choice.
    Returns True if the player wins the game, False otherwise.
    """
    usable_items = logic.get_usable_items(state["pockets"])
    craftable_items = logic.get_craftable_items(state["pockets"])

    actions = ["Move to another room", "Explore the room", "View your pockets"]

    if usable_items:
        actions.append("Use an item")
    if craftable_items:
        actions.append("Craft an item from the items in your pockets")

    actions.append("Exit the game")

    menus.user_choice_prompt(actions)
    choice = actions[menus.prompt_choice(len(actions)) - 1]

    if choice == "Move to another room":
        move_room(state)

    elif choice == "Explore the room":
        explore_room(state)

    elif choice == "View your pockets":
        menus.view_pockets_menu(state["pockets"])

    elif choice == "Use an item":
        return use_item(state, usable_items)

    elif choice == "Craft an item from the items in your pockets":
        craft_item(state, craftable_items)

    else:  # Exit the game
        logic.exit_game()

    return False


def run_game() -> None:
    """
    Run the main game loop: show the main menu, then run the game until the player wins or exits.
    """
    while True:
        state = main_menu_loop()

        while True:
            if play_turn(state):
                record_win(state)
                break


if __name__ == "__main__":
    """
    Entry point for the game.
    """
    try:
        run_game()
    except (KeyboardInterrupt, EOFError):
        print()
        logic.exit_game(delay=0)
