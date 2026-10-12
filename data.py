"""
KeyError: The Keeper of the Golden Key
data.py

Static game data:
the hospital layout, objects, items and crafting recipes.
"""

# Hospital Layout
# Each room maps to its exits as (direction arrow, destination room) pairs.
# Arrows follow the layout drawn by the in-game map. Exits are two-way.
rooms: dict[str, list[tuple[str, str]]] = {
    "Hospital Reception": [("↙", "Waiting Room"), ("↘", "Cafeteria")],
    "Waiting Room": [("↗", "Hospital Reception"), ("→", "Cafeteria"), ("↓", "Patient Ward")],
    "Cafeteria": [("↖", "Hospital Reception"), ("←", "Waiting Room")],
    "Patient Ward": [("↑", "Waiting Room"), ("↙", "Operating Theater"), ("↘", "Storage Room")],
    "Operating Theater": [("↑", "Patient Ward"), ("→", "Storage Room")],
    "Storage Room": [("↑", "Patient Ward"), ("←", "Operating Theater")],
}

# The room where the Golden Key opens the exit door.
exit_room = "Hospital Reception"

# Number of objects per room.
# Every room holds objects_per_room of these, each hiding one item.
objects_per_room = 2

# Searchable objects with descriptions.
room_objects: dict[str, str] = {
    "Filing Cabinet": "A rusted cabinet, its drawers hanging open.",
    "Medical Trolley": "A trolley with one wobbly wheel and a tray of dusty instruments.",
    "Desk": "A heavy wooden desk buried under mouldering paperwork.",
    "Locker": "A dented staff locker, its door hanging off one hinge.",
    "Chair": "A torn leather chair with the stuffing spilling out.",
    "Vending Machine": "A vending machine with a cracked screen",
}

# Every item the player can find or craft with its description.
items: dict[str, str] = {
    "Keycard": "A staff keycard, the name long since worn away.",
    "Surgical Glue": "A tube of medical-grade adhesive. It could hold almost anything together.",
    "Fire Extinguisher": "Heavy, red and, sadly, empty.",
    "Golden Key Piece": "A shard of a golden key. There must be more pieces somewhere.",
    "Map": "A folded map of the hospital floor plan.",
    "Crowbar": "A solid steel crowbar. Useful, if only something needed prying open.",
    "First Aid Kit": "A kit with a few unexpired bandages.",
    "Flashlight": "It works, but only just.",
    "Scalpel": "Still sharp. You handle it with care.",
    "Hammer": "A claw hammer with a taped handle.",
    "Golden Key": "A key of solid gold. It looks like it opens something very important.",
}

essential_items = ["Golden Key Piece", "Golden Key Piece", "Golden Key Piece", "Surgical Glue"]

usable_items = ["Map", "Golden Key"]

crafting_recipes: dict[str, dict[str, int]] = {
    "Golden Key": {"Golden Key Piece": 3, "Surgical Glue": 1},
}

crafted_items = set(crafting_recipes)
