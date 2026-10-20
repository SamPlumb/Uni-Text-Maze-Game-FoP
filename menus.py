"""
KeyError: The Keeper of the Golden Key
menus.py

Menu states for the game:
main menus, room navigation, object investigation, item usage and crafting.
"""
from random import choice as random_choice

import data
import text
from prompts import enter_choice_prompt
from ui import bold, show_menu, divider


def join_phrases(phrases: list[str]) -> str:
    """
    Join a list of phrases into a single string with commas and 'and'.
    If the list is empty, return an empty string. If it has one item, return that item.
    If it has two items, join them with 'and'. If it has more than two items, join all but the last with commas and
    add 'and' before the last item.
    """
    if len(phrases) <= 2:
        return " and ".join(phrases)
    return ", ".join(phrases[:-1]) + f", and {phrases[-1]}"


def with_article(phrase: str) -> str:
    """
    Add 'a' or 'an' to the start of a phrase based on its first letter.
    If the first letter is a vowel, use 'an', otherwise use 'a'.
    """
    if phrase[0].lower() in "aeiou":
        return f"an {phrase}"
    else:
        return f"a {phrase}"


def numbered_list(items: list[str]) -> list[str]:
    """
    Number a list of items
    Return a list of strings where each item is prefixed with its number in the list (starting from 1).
    """
    return [f"{i}. {item}" for i, item in enumerate(items, 1)]


def format_duration(seconds: int) -> str:
    """
    Format a duration in seconds into a human-readable string.
    Returns a string in the format "Xh Ym Zs" where X is hours, Y is minutes, and Z is seconds.
    If hours are zero, they are omitted. If minutes are zero, they are omitted.
    """
    hours, remainder = divmod(int(seconds), 3600)
    minutes, sec = divmod(remainder, 60)

    if hours:
        return f"{hours}h {minutes}m {sec}s"

    if minutes:
        return f"{minutes}m {sec}s"

    return f"{sec}s"


def main_menu(options: list[str]) -> None:
    """
    Display the main menu with the game title, description, and options.
    """
    show_menu([
        bold("Welcome to KeyError: The Keeper of the Golden Key!"),
        divider,
        "In this game, you will explore an abandoned hospital, searching for items and clues to escape. "
        "You will need to find and craft items, and use them wisely to unlock doors and progress through the hospital. "
        "Be careful, as some items may be hidden or require specific actions to obtain.",
        divider,
        *numbered_list(options),
        divider,
        enter_choice_prompt(len(options))])


def game_intro() -> None:
    """
    Display the game introduction text.
    """
    show_menu(
        [random_choice(text.intro_text),
         divider,
         "You must find a way to escape the hospital and uncover the mystery of how you got here."])


def leaderboard_lines(entries: list[dict]) -> list[str]:
    """
    Return a list of strings representing the leaderboard entries.
    Each entry is formatted as "Rank. Name - Time seconds".
    """
    return [f"{i}. {entry['name']} - {format_duration(entry['time'])}"
            for i, entry in enumerate(entries, 1)]


def display_leaderboard(entries: list[dict]) -> None:
    """
    Display the leaderboard entries in a box.
    If the leaderboard is empty, display a message indicating that, else display the entries in a numbered list.
    """
    if not entries:
        show_menu(
            [bold("The leaderboard is currently empty.")])

    else:
        show_menu(
            [bold("Leaderboard:"),
             divider,
             *leaderboard_lines(entries)])


def remove_leaderboard_entry_menu(entries: list[dict]) -> None:
    """
    Display the leaderboard entries and prompt the player to select one to remove.
    """
    show_menu(
        [bold("Remove a Leaderboard Entry:"),
         divider,
         *leaderboard_lines(entries),
         f"{len(entries) + 1}. Back",
         divider,
         enter_choice_prompt(len(entries) + 1)])


def you_win_menu(seconds: int) -> None:
    """
    Display the win screen and prompt the player to enter their name for the leaderboard.
    """
    show_menu([
        "The golden key fits the lock on the hospital reception door, it opens. "
        "Sunlight blinds your vision as you step through... "
        "The door slams shut, as your eyes adjust to your new surroundings.",
        divider,
        bold("You have escaped the hospital!"),
        f"Your time was {format_duration(seconds)}.",
        divider,
        "Please enter your name to record your score on the leaderboard:"])


def move_room_menu(current_room: str, exits: list[tuple[str, str]]) -> None:
    """
    Display the move room menu, showing the current room and its exits.
    """
    exit_names = [exit_name for _, exit_name in exits] + ["Stay in the current room"]
    name_width = max(len(name) for name in exit_names)

    show_menu(
        [random_choice(text.move_room_text),
         divider,
         *[f"{arrow} {exit_name:{name_width}}" for arrow, exit_name in exits],
         divider])

    show_menu([f"You are currently in the {bold(current_room)}.",
               divider,
               "Where would you like to go?",
               *numbered_list(exit_names),
               divider,
               enter_choice_prompt(len(exit_names))])


def room_description(room: str, exits: list[tuple[str, str]], objects: list[str]) -> str:
    """
    Display the room description and the objects in the room.
    If the room has a unique description, use that. Otherwise, generate a random description.
    """
    objects_phrase = join_phrases([with_article(obj) for obj in objects])

    if room in text.unique_room_text:
        return text.unique_room_text[room].format(objects=objects_phrase)

    exit_names = join_phrases([name.lower() for _, name in exits])
    description = random_choice(text.room_description_text)
    return description.format(room=room.lower(), objects=objects_phrase, exit_names=exit_names)


def explore_room_menu(room: str, exits: list[tuple[str, str]], objects: list[str]) -> None:
    """
    Display the explore room menu, showing the room description and the objects in the room.
    """
    description = room_description(room, exits, objects)

    show_menu(
        [description,
         divider,
         "What would you like to investigate?",
         *numbered_list(objects + ["Back"]),
         divider,
         enter_choice_prompt(len(objects) + 1)])


def investigate_object_menu(object_name: str, item_name: str | None) -> None:
    """
    Display the investigate object menu, showing the object and the item found (if any).
    """
    if item_name is None:
        show_menu(
            [f"You approach the {object_name.lower()}, but it seems to be empty.",
             divider,
             "It seems that you have already searched this object before."])
        return

    show_menu(
        [f"{data.room_objects[object_name]} As you examine more closely, you see something hidden within it.",
         divider,
         data.items[item_name],
         f"You put the {bold(item_name.lower())} in your pocket."])


def view_pockets_menu(pockets: dict[str, int]) -> None:
    """
    Display the player's pockets in a numbered list.
    """
    held_items = {item: qty for item, qty in pockets.items() if qty > 0}

    if not held_items:
        show_menu(["Your pockets are empty."])
        return

    show_menu(
        [bold("Your Pockets:"),
         divider,
         *([f"{item} x{qty}" for item, qty in held_items.items()]),
         divider])


def user_choice_menu(choices: list[str]) -> None:
    """
    Within the main game option menu, prompt the user for a choice from a list of numbered options.
    """
    num_choices = len(choices)
    show_menu(
        [bold("What would you like to do?"),
         divider,
         *numbered_list(choices),
         divider,
         enter_choice_prompt(num_choices)])


def item_choice_menu(menu_title: str, items: list[str]) -> None:
    """
    shared menu for item usage and crafting, displays a list of items and prompts the user to choose one.
    """
    show_menu(
        [bold(menu_title),
         divider,
         *numbered_list(items + ["Back"]),
         divider,
         enter_choice_prompt(len(items) + 1)])


def crafting_menu(craftable_items: list[str]) -> None:
    """
    Display the crafting menu, showing the craftable items.
    """
    item_choice_menu("Crafting Menu", craftable_items)


def use_item_menu(usable_items: list[str]) -> None:
    """
    Display the use item menu, showing the usable items.
    """
    item_choice_menu("Use Item Menu", usable_items)


def open_map() -> None:
    """
    Display the map of the hospital.
    """
    show_menu([
        "You unfold the map and see a layout of the hospital.",
        divider,
        *text.game_map_art
    ])
