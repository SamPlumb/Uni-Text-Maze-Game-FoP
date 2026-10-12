"""
Keyerror: The Keeper of the Golden Key
menus.py

Menu states for the game:
main menu, room navigation, object investigation, item usage and crafting.
"""
import random

import data
import logic
from ui import bold, d_box, menu_delay

divider = "-" * 30

# Text for the game introduction, room movement, and unique room descriptions.
intro_text = [
    "You find yourself waking up in a strange place, not knowing how you got here. "
    "Disoriented and frightened, a sense of urgency fills your mind. "
    "As you look around, you realise that you are trapped in an abandoned hospital "
    "with no way out.",

    "Looking around, you realise that you are in a never-ending abandoned hospital. "
    "It seems like you have been here for a while, "
    "but you have no memory of how you got here or why.",

    "Confused about how you arrived here and with no memory of your past, "
    "you feel a growing sense of curiosity and unease. "
    "It appears to be a hospital, only recognisable by its clinical wallpaper, "
    "but it seems abandoned, old and decrepit, with peeling paint and broken windows.",

    "You wake up in a dimly lit room, your head throbbing with pain and confusion. "
    "As you look around, you see that you are in an abandoned hospital room "
    "with doorways leading to different parts of the hospital.",
]

move_room_text = [
    "You look around the room, searching for any possible exits. "
    "After a moment of searching, you find the following exits:",

    "You take a moment to gather your thoughts and plan your next move. "
    "You see the following exits from the current room:",

    "You take a deep breath and decide to move to another room. "
    "You see the following exits from the current room:",
]

room_description_text = [
    "The {room} is dimly lit, with flickering lights casting eerie shadows on the walls. "
    "You notice a few objects scattered around the room, including {objects}. "
    "There are exits to the {exit_names}.",

    "The {room} is filled with a musty smell, and you can hear the sound of dripping water echoing through the halls. "
    "You notice {objects} in the room, and there are exits to the {exit_names}.",

    "The {room} is quiet, except for the sound of your own breathing. "
    "You notice {objects} in the room, and there are exits to the {exit_names}.",
]

unique_room_text = {
    "Storage Room":
        "The tiny storage room is pitch black with the only light coming from its two "
        "doorways, one leading to an operating theater and the other to the patient ward. "
        "Trying to find your way around the room you stumble into {objects}.",

    "Hospital Reception":
        "As your eyes adjust from the bright light shining through the massive windows, "
        "you notice two big welcome desks with barrier ropes strung across the floor. "
        "You think that you must be at the hospital reception and immediately try to find "
        "a way out, but you can only find a door with a massive almost mythical padlock... "
        "It seems like there are only two other exits, to a waiting room and a cafeteria. "
        "Near the door you notice {objects}."
}

win_text = [
    "The golden key fits the lock on the hospital reception door, it opens. "
    "Sunlight blinds your vision as you step through..."
    "The door slams shut, as your eyes adjust to your new surroundings."
]


def join_phrases(phrases: list[str]) -> str:
    """
    Join a list of phrases into a single string with commas and 'and'.
    If the list is empty, return an empty string. If it has one item, return that item.
    If it has two items, join them with 'and'. If it has more than two items, join all but the last with commas and
    add 'and' before the last item.
    """
    if len(phrases) == 0:
        return ""
    elif len(phrases) == 1:
        return phrases[0]
    elif len(phrases) == 2:
        return f"{phrases[0]} and {phrases[1]}"
    else:
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
    return [f"{i + 1}. {item}" for i, item in enumerate(items)]


def enter_choice_prompt(num_options: int) -> str:
    """
    Prompt the user to enter a choice.
    """
    return f"Please enter your choice (1-{num_options}):"


def main_menu() -> None:
    """
    Display the main menu and return the player's choice.
    """
    menu_delay()
    d_box([
        bold("Welcome to Keyerror: The Keeper of the Golden Key!"),
        divider,
        "In this game, you will explore an abandoned hospital, searching for items and clues to escape.",
        "You will need to find and craft items, and use them wisely to unlock doors and progress through the hospital.",
        "Be careful, as some items may be hidden or require specific actions to obtain.",
        divider,
        *numbered_list([
            "Start a new game",
            "View Leaderboard",
            "Remove a Leaderboard Entry",
            "Exit the game"]),
        divider,
        "Please enter the number of your choice (1-4):"])


def game_intro() -> None:
    """
    Display the game introduction text.
    """
    menu_delay()
    d_box([
        random.choice(intro_text),
        divider,
        "You must find a way to escape the hospital and uncover the mystery of how you got here."])


def leaderboard_lines(entries: list[dict]) -> list[str]:
    """
    Return a list of strings representing the leaderboard entries.
    Each entry is formatted as "Rank. Name - Time seconds".
    """
    lines = []
    for i, entry in enumerate(entries):
        lines.append(f"{i + 1}. {entry['name']} - {logic.format_duration(entry['time'])}")

    return lines


def display_leaderboard(entries: list[dict]) -> None:
    """
    Display the leaderboard entries in a box.
    If the leaderboard is empty, display a message indicating that, else display the entries in a numbered list.
    """
    menu_delay()
    if not entries:
        d_box([bold("The leaderboard is currently empty.")])

    else:
        d_box([bold("Leaderboard:"),
               divider,
               *leaderboard_lines(entries)])


def remove_leaderboard_entry_menu(entries: list[dict]) -> None:
    """
    Display the leaderboard entries and prompt the player to select one to remove.
    """
    menu_delay()
    d_box([bold("Remove a Leaderboard Entry:"),
           divider,
           *leaderboard_lines(entries),
           f"{len(entries) + 1}. Back",
           divider,
           enter_choice_prompt(len(entries) + 1)])


def you_win_menu(seconds: int) -> None:
    """
    Display the win screen and prompt the player to enter their name for the leaderboard.
    """
    menu_delay()
    d_box([
        random.choice(win_text),
        divider,
        bold("You have escaped the hospital!"),
        f"Your time was {logic.format_duration(seconds)}.",
        divider,
        "Please enter your name to record your score on the leaderboard:"])


def user_choice_prompt(choices: list[str]) -> None:
    """
    Within the main game option menu, prompt the user for a choice from a list of numbered options.
    """
    num_choices = len(choices)
    menu_delay()
    d_box([bold("What would you like to do?"),
           divider,
           *numbered_list(choices),
           divider,
           enter_choice_prompt(num_choices)])


def move_room_menu(current_room: str) -> None:
    """
    Display the move room menu, showing the current room and its exits.
    """
    exits = logic.current_room_exits(current_room)
    exit_names = [exit_name for _, exit_name in exits] + ["Stay in the current room"]
    name_width = max(len(name) for name in exit_names)

    menu_delay()
    d_box([random.choice(move_room_text),
           divider,
           *[f"{arrow} {exit_name:{name_width}}" for arrow, exit_name in exits],
           divider])

    menu_delay()
    d_box([f"You are currently in the {bold(current_room)}.",
           divider,
           "Where would you like to go?",
           *numbered_list(exit_names),
           divider,
           enter_choice_prompt(len(exit_names))])


def room_description_menu(room: str, objects: list[str]) -> str:
    """
    Display the room description and the objects in the room.
    If the room has a unique description, use that. Otherwise, generate a random description.
    """
    room_lower = room.lower()
    object_names = [with_article(object_name) for object_name in objects]
    exit_names = join_phrases([name.lower() for _, name in logic.current_room_exits(room)])
    objects_phrase = join_phrases(object_names)

    if room in unique_room_text:
        return unique_room_text[room].format(objects=join_phrases([with_article(obj) for obj in objects]))

    else:
        room_description = random.choice(room_description_text)
        return room_description.format(room=room_lower, objects=objects_phrase, exit_names=exit_names)


def explore_room_menu(room: str, objects: list[str]) -> None:
    """
    Display the explore room menu, showing the room description and the objects in the room.
    """
    description = room_description_menu(room, objects)

    menu_delay()
    d_box([description,
           divider,
           "What would you like to investigate?",
           *numbered_list(objects + ["Back"]),
           divider,
           enter_choice_prompt(len(objects) + 1)])


def investigate_object_menu(object_name: str, item_name: str | None) -> None:
    """
    Display the investigate object menu, showing the object and the item found (if any).
    """
    menu_delay()
    if item_name is None:
        d_box([f"You approach the {object_name.lower()}, but it seems to be empty.",
               divider,
               "It seems that you have already searched this object before."
               ])
        return
    else:
        d_box([f"{data.room_objects[object_name]} As you examine more closely, you see something hidden within it.",
               divider,
               data.items[item_name],
               f"You put the {bold(item_name.lower())} in your pocket."
               ])


def view_pockets_menu(pockets: dict[str, int]) -> None:
    """
    Display the player's pockets in a numbered list.
    """
    held_items = {item: qty for item, qty in pockets.items() if qty > 0}

    if not held_items:
        d_box(["Your pockets are empty."])
        return

    menu_delay()
    d_box([bold("Your Pockets:"),
           divider,
           *([f"{item} x{qty}" for item, qty in held_items.items()]),
           divider])


def item_choice_menu(menu_title: str, items: list[str]) -> None:
    """
    shared menu for item usage and crafting, displays a list of items and prompts the user to choose one.
    """
    menu_delay()
    d_box([bold(menu_title),
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
    menu_delay()
    d_box([
        "You unfold the map and see a layout of the hospital.",
        divider,
        "              ┌─────────  ────────┐ ",
        "              │                   │ ",
        "              │  Hotel Reception  │ ",
        "              │   ▲           ▲   │ ",
        "┌─────────────┴── │ ┬──────── │ ──┴┐",
        "│                 ▼ │         ▼    │",
        "│  Waiting Room     │   Cafeteria  │",
        "│                 ◄───►            │",
        "│        ▲          ├──────────────┘",
        "└─┬───── │ ─────────┴──────────────┐",
        "  │      ▼                         │",
        "  │                Patient Ward    │",
        "  │              ▲             ▲   │",
        "┌─┴───────────── │ ────┬────── │ ─┬┘",
        "│                ▼     │       ▼  │ ",
        "│  Operating Theater   │   Storage│ ",
        "│                    ◄───► Room   │ ",
        "│                      ├──────────┘ ",
        "└──────────────────────┘            "
    ])


def invalid_choice(user_input: str, num_choices: int) -> None:
    """
    Display a message for an invalid menu choice.
    """
    menu_delay()
    d_box([f"Invalid choice: '{user_input}'.",
           divider,
           enter_choice_prompt(num_choices)])


def prompt_choice(num_choices: int) -> int:
    """
    Prompt the user for a menu choice and validate the input.
    Returns the valid choice as an integer.
    """
    while True:
        user_choice = input().strip()
        if user_choice.isdigit() and 1 <= int(user_choice) <= num_choices:
            return int(user_choice)
        invalid_choice(user_choice, num_choices)
