"""
KeyError: The Keeper of the Golden Key
game.py

Core game loop:
connects the menus, prompts and logic modules to run the game.
"""
from collections.abc import Callable
from sys import exit as sys_exit
from typing import NoReturn

import leaderboard
import logic
import menus
import prompts
from ui import show_menu, bold, menu_delay


def main_menu_loop() -> dict:
    """
    Run the main menu until the player starts a game, and return the new game state.
    Prompts the player to choose from the main menu options:
    new game, leaderboard, remove leaderboard entry, or exit the game.
    """
    options: list[tuple[str, Callable[[], dict | None]]] = [
        ("Start a new game", start_new_game),
        ("View the leaderboard", view_leaderboard),
        ("Remove a Leaderboard Entry", remove_leaderboard_entry),
        ("Exit the game", exit_game)
    ]

    while True:
        menus.main_menu([label for label, _ in options])
        _, handler = options[prompts.prompt_choice(len(options)) - 1]
        state = handler()

        if state is not None:
            return state


def exit_game(delay: float = 3) -> NoReturn:
    """
    Exit the game.
    """
    show_menu([bold("Thank you for playing KeyError!"), "Exiting Game..."])
    menu_delay(delay)
    sys_exit()


def start_new_game() -> dict:
    """
    Start a new game and return the initial game state.
    """
    state = logic.new_game()
    menus.game_intro()
    return state


def view_leaderboard() -> None:
    """
    Display the leaderboard.
    """
    entries = leaderboard.load()
    menus.display_leaderboard(entries)


def remove_leaderboard_entry() -> None:
    """
    Remove a leaderboard entry.
    """
    entries = leaderboard.load()

    if not entries:
        menus.display_leaderboard(entries)
        return

    menus.remove_leaderboard_entry_menu(entries)
    choice = prompts.prompt_choice(len(entries) + 1)

    if choice == len(entries) + 1:  # Return to the main menu
        return

    if leaderboard.remove_score(entries[choice - 1]):
        show_menu(["The leaderboard entry has been removed from the leaderboard."])
    else:
        show_menu(["That entry could not be found in the leaderboard."])


def record_win(state: dict) -> None:
    """
    Show the win screen and save the player's time under the name they enter.
    """
    seconds = logic.game_timer(state)
    menus.you_win_menu(seconds)
    name = prompts.prompt_name()

    try:
        leaderboard.add_score(name, seconds)
    except OSError as error:
        show_menu([f"Could not save score: {error}"])


def move_room(state: dict) -> bool:
    """
    Show the move room menu and update the game state based on the player's choice.
    Returns False, as moving rooms does not result in a win condition.
    """
    exits = logic.current_room_exits(state["room"])
    menus.move_room_menu(state["room"], exits)
    choice = prompts.prompt_choice(len(exits) + 1)

    if choice == len(exits) + 1:  # choose to not move, return to the game menu
        return False

    old_room = state["room"]
    logic.move_player_room(state, exits[choice - 1][1])
    show_menu([f"You have left the {old_room} and entered the {state['room']}."])
    return False


def explore_room(state: dict) -> bool:
    """
    Show the explore room menu and update the game state based on the player's choice.
    Returns False as exploring a room does not result in a win condition.
    """
    objects = state["room_objects"][state["room"]]
    exits = logic.current_room_exits(state["room"])
    menus.explore_room_menu(state["room"], exits, objects)

    choice = prompts.prompt_choice(len(objects) + 1)

    if choice == len(objects) + 1:  # choose to not investigate any object, return to the game menu
        return False

    index = choice - 1
    item = logic.pick_up_item(state, index)
    menus.investigate_object_menu(objects[index], item)
    return False


def use_item(state: dict, usable_items: list[str]) -> bool:
    """
    Show the use item menu and update the game state based on the player's choice.
    Returns True if the player wins the game, False otherwise.
    """
    menus.use_item_menu(usable_items)
    choice = prompts.prompt_choice(len(usable_items) + 1)

    if choice == len(usable_items) + 1:  # No item to use, return to game menu
        return False

    outcome = logic.use_item(state, usable_items[choice - 1])

    if outcome == logic.use_map:
        menus.open_map()
    elif outcome == logic.use_no_lock:
        show_menu(["You try to use the Golden Key, but it doesn't fit any lock in this room."])
    elif outcome == logic.use_invalid:
        show_menu(["You cannot use that item."])

    return outcome == logic.use_win


def craft_item(state: dict, craftable_items: list[str]) -> bool:
    """
    Show the crafting menu and update the game state based on the player's choice.
    Returns False, as crafting an item does not result in a win condition.
    """
    menus.crafting_menu(craftable_items)
    choice = prompts.prompt_choice(len(craftable_items) + 1)

    if choice == len(craftable_items) + 1:  # choose to not craft any item, return to the game menu
        return False

    item = craftable_items[choice - 1]

    if logic.craft_item(state["pockets"], item):
        show_menu([f"You have successfully crafted a {item}."])
    else:
        show_menu([f"You do not have the necessary ingredients to craft a {item}."])

    return False


def view_pockets(state: dict) -> bool:
    """
    Show the player's pockets
    Returns False, as viewing pockets does not result in a win condition.
    """
    menus.view_pockets_menu(state["pockets"])
    return False


def play_turn(state: dict) -> bool:
    """
    Show the game menu and update the game state based on the player's choice.
    Returns True if the player wins the game, False otherwise.
    """
    usable_items = logic.get_usable_items(state["pockets"])
    craftable_items = logic.get_craftable_items(state["pockets"])

    actions: list[tuple[str, Callable[[], bool]]] = [
        ("Move to another room", lambda: move_room(state)),
        ("Explore the room", lambda: explore_room(state)),
        ("View your pockets", lambda: view_pockets(state))]

    if usable_items:
        actions.append(("Use an item", lambda: use_item(state, usable_items)))
    if craftable_items:
        actions.append(("Craft an item from the items in your pockets", lambda: craft_item(state, craftable_items)))

    actions.append(("Exit the game", lambda: exit_game()))

    menus.user_choice_menu([label for label, _ in actions])
    _, handler = actions[prompts.prompt_choice(len(actions)) - 1]

    return handler()  # Execute the chosen action and return its result


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
    # Entry point for the game.
    try:
        run_game()
    except (KeyboardInterrupt, EOFError):
        print()
        exit_game(delay=0)
