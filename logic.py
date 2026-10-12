"""
KeyError: The Keeper of the Golden Key
logic.py

Core game functions:
exit, new_game, move room, craft and use items, game timer and random distribution of objects and items.
"""

from collections import Counter
from random import Random
from sys import exit as sys_exit
from time import sleep, monotonic

import data
from ui import bold, d_box

# Outcome of using an item
use_win = "win"
use_map = "map"
use_no_lock = "no_lock"
use_invalid = "invalid"


def exit_game(delay: float = 3) -> None:
    """
    Exit the game.
    """
    d_box([bold("Thank you for playing KeyError!"), "Exiting Game..."])
    sleep(delay)
    sys_exit()


def new_game(rng: Random | None = None) -> dict:
    """
    Build a fresh game state: random spawn room, shuffled objects and items, and start timer.
    Returns a dictionary representing the game state.
    """
    rng = rng or Random()
    rooms = list(data.rooms)

    return {
        "room": rng.choice(rooms),
        "pockets": Counter(),
        "room_objects": distribute_objects(rng, rooms),
        "room_items": distribute_items(rng, rooms),
        "start_time": monotonic(),
    }


def distribute_objects(rng: Random, rooms: list[str]) -> dict[str, list[str]]:
    """
    Give each room objects_per_room amount of different objects.
    Returns a dictionary mapping room names to lists of objects.
    """
    return {room: rng.sample(list(data.room_objects), data.objects_per_room) for room in rooms}


def distribute_items(rng: Random, rooms: list[str]) -> dict[str, list[str]]:
    """
    Hide one item in each object, guaranteeing the items needed to win are placed.
    Raises ValueError if there aren't enough hiding places for the essential items.
    Returns a dictionary mapping room names to lists of items.
    """
    # Calculate the total number of item slots available in all rooms
    item_slots = len(rooms) * data.objects_per_room

    # Check if there are enough hiding places for the essential items
    if item_slots < len(data.essential_items):
        raise ValueError("Not enough hiding places for the essential items.")

    # Filler items exclude anything essential or crafted, and repeat if there are spare slots
    filler_pool = [item for item in data.items
                   if item not in data.essential_items and item not in data.crafted_items]
    filler = []

    while len(filler) < item_slots - len(data.essential_items):
        filler.extend(rng.sample(filler_pool, len(filler_pool)))

    # Combine essential items with filler items and shuffle them
    items = data.essential_items + filler[:item_slots - len(data.essential_items)]
    rng.shuffle(items)

    # Distribute the items into the rooms, ensuring each room gets the correct number of items
    per_room = data.objects_per_room

    return {room: items[i * per_room:(i + 1) * per_room] for i, room in enumerate(rooms)}


def current_room_exits(room: str) -> list[tuple[str, str]]:
    """
    Return the exits from the given room.
    """
    return data.rooms[room]


def move_player_room(state: dict, new_room: str) -> None:
    """
    Move the player to a new room and update the game state.
    Raises ValueError if the new room is not a valid exit from the current room.
    """
    # Check if the new room is a valid exit from the current room
    if new_room not in [name for _, name in current_room_exits(state["room"])]:
        raise ValueError(f"Cannot move to {new_room} from {state['room']}.")

    # Update the player's current room in the game state
    state["room"] = new_room


def pick_up_item(state: dict, object_index: int) -> str | None:
    """
    Pick up an item from the current room's object at the given index and add it to the player's pockets.
    Returns the item's name if successfully picked up, or None if the object has already been searched.
    """
    items_in_room = state["room_items"][state["room"]]
    item = items_in_room[object_index]

    # If the item is not None, add it to the player's pockets and remove it from the room
    if item is not None:
        state["pockets"][item] += 1
        items_in_room[object_index] = None  # Remove the item from the room after picking it up
        return item

    # If the item is None, it means the object has already been searched, so return None
    return None


def get_usable_items(pockets: Counter) -> list[str]:
    """
    Returns a list of item names that are both in the player's pockets and
    in the list of usable items defined in the game data.
    """
    return [item for item in pockets if item in data.usable_items and pockets[item] > 0]


def can_craft_item(pockets: Counter, item: str) -> bool:
    """
    Check if the player can craft the given item with their current pockets.
    Returns True if the player has all the required ingredients in sufficient quantities, False otherwise.
    """
    recipe = data.crafting_recipes.get(item)

    # If the item does not have a recipe, it cannot be crafted
    if not recipe:
        return False
    # If the recipe exists, check if the player has enough of each ingredient
    else:
        return all(pockets[ingredient] >= qty for ingredient, qty in recipe.items())


def get_craftable_items(pockets: Counter) -> list[str]:
    """
    Return a list of craftable items based on the player's pockets.
    """
    return [item for item in data.crafting_recipes if can_craft_item(pockets, item)]


def craft_item(pockets: Counter, item: str) -> bool:
    """
    Craft an item using the player's pockets.
    Crafting ingredients are deducted from the pockets, and the crafted item is added.
    Returns True if crafting was successful, False if the player does not have the required ingredients.
    """
    # Check if the player can craft the item
    if not can_craft_item(pockets, item):
        return False

    recipe = data.crafting_recipes[item]

    for ingredient, qty in recipe.items():
        pockets[ingredient] -= qty  # Deduct the ingredients from the pockets

    pockets[item] += 1  # Add the crafted item to the pockets
    return True


def use_item(state: dict, item: str) -> str:
    """
    Use an item from the player's pockets and return the outcome.
    Possible outcomes:
    Golden Key:
    - use_win: The player wins the game by using the item in the correct room.
    - use_no_lock: The player tries to use a key in a room without a lock.
    Map:
    - use_map: The player uses the map to view the game map.
    Invalid usage:
    - use_invalid: The item cannot be used or is not in the player's pockets.
    """
    if item not in data.usable_items or state["pockets"][item] <= 0:
        return use_invalid

    if item == "Golden Key":

        # Check if the player is in a room with a lock that can be opened
        if state["room"] in data.exit_room:
            state["pockets"][item] -= 1  # Use the key
            return use_win  # Player wins by using the key

        else:
            return use_no_lock  # No lock to open in this room

    elif item == "Map":
        return use_map  # Show the map

    return use_invalid


def game_timer(state: dict) -> int:
    """
    Return the time since the game started.
    """
    return int(monotonic() - state["start_time"])


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
