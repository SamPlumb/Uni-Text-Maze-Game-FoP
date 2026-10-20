"""
KeyError: The Keeper of the Golden Key
leaderboard.py

functions to manage leaderboard interaction:
load, save, add and remove and verify entries.
"""

import json
import os
from pathlib import Path

# The default file is in the same directory as this module
default_file = Path(__file__).resolve().parent / "leaderboard.json"

# Variable for the maximum length of a player name
max_name_length = 20


def clean_name(name: str) -> str:
    """
    Clean a player name by stripping whitespace.
    """
    return " ".join(name.split())


def validate_player_name(name: str) -> str | None:
    """
    Check if a player name is valid.
    Returns an error message if the name is invalid, otherwise returns None.
    """
    if not name:
        return "Player name cannot be blank."
    if len(name) > max_name_length:
        return f"Player name cannot be longer than {max_name_length} characters."
    if not name.replace(" ", "").isalnum():
        return "Player name can only contain letters, numbers, and spaces."
    return None  # Valid name


def is_valid_entry(entry: object) -> bool:
    """
    Check if an entry is a valid leaderboard entry.
    Returns True if the entry is a dict with a non-empty string 'name' and no longer than max_name_length characters,
    and a numeric 'time' that is zero or greater.
    """
    if not isinstance(entry, dict):
        return False

    name = entry.get("name")
    time = entry.get("time")

    valid_name = isinstance(name, str) and 0 < len(name) <= max_name_length and name.isprintable()
    valid_time = isinstance(time, (int, float)) and time >= 0

    return valid_name and valid_time


def sort_entries(entries: list[dict]) -> list[dict]:
    """
    Sort entries by time in ascending order (fastest first).
    Returns a new list of sorted entries.
    """
    return sorted(entries, key=lambda entry: entry["time"])


def valid_sorted_entries(entries: list[dict]) -> list[dict]:
    """
    Filter out invalid entries and return a sorted list of valid entries.
    Returns a new list of valid entries sorted by time (fastest first).
    """
    valid_entries = [entry for entry in entries if is_valid_entry(entry)]

    return sort_entries(valid_entries)


def load(filename: Path | str | None = None) -> list[dict]:
    """
    Load entries sorted fastest first.
    A missing file gives an empty board. An unreadable file renamed to 'filename.corrupt'
    rather than being overwritten by the next save and gives an empty board.
    """
    path = Path(filename or default_file)

    try:
        with path.open(encoding="utf-8") as file:
            entries = json.load(file)

    # If the file doesn't exist, return an empty leaderboard
    except FileNotFoundError:
        return []

    # If the file is corrupt, rename it and return an empty leaderboard
    except (json.JSONDecodeError, UnicodeDecodeError):
        os.replace(path, path.with_name(path.name + ".corrupt"))
        return []

    # If the loaded data is not a list, return an empty leaderboard
    if not isinstance(entries, list):
        return []

    # Filter out invalid entries and sort the valid ones by time (fastest first)
    return valid_sorted_entries(entries)


def save(entries: list[dict], filename: Path | str | None = None) -> None:
    """
    Saves entries sorted fastest first.
    Writes to a temporary file first so a crash can't leave a half-written leaderboard.
    Raises OSError if the file can't be written.
    """
    path = Path(filename or default_file)
    temp_path = path.with_name(path.name + ".tmp")

    # Write the valid sorted entries to a temporary file
    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(valid_sorted_entries(entries), file, indent=4)

    # Replace the original file with the temporary file
    os.replace(temp_path, path)


def add_score(name: str, seconds: int, filename: Path | str | None = None) -> None:
    """
    Record a score.
    Raises ValueError for a blank name, name longer than max_name_length, invalid characters, or negative time.
    Raises OSError if the file can't be written.
    """
    plr_name = clean_name(name)

    error = validate_player_name(plr_name)
    if error:
        raise ValueError(error)

    if seconds < 0:
        raise ValueError("Score cannot be negative.")

    entries = load(filename)
    entries.append({"name": plr_name, "time": seconds})
    save(entries, filename)


def remove_score(entry: dict, filename: Path | str | None = None) -> bool:
    """
    Remove a specific entry from the leaderboard.
    Returns True if the entry was found and removed,
    False if the entry is not found.
    """
    entries = load(filename)

    if entry in entries:
        entries.remove(entry)
        save(entries, filename)
        return True

    return False
