"""
KeyError: The Keeper of the Golden Key
text.py

Flavor text for the game:
Holds all the menu text.
"""

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

game_map_art = [
    "              ┌─────────  ────────┐ ",
    "              │                   │ ",
    "              │     Reception     │ ",
    "              │   ▲           ▲   │ ",
    "┌─────────────┴── │ ┬──────── │ ──┴┐",
    "│                 ▼ │         ▼    │",
    "│   Waiting Room    │   Cafeteria  │",
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
]
