"""
Keyerror: The Keeper of the Golden Key
leaderboard.py

functions to manage leaderboard interaction:
load, save, add and remove and verify entries.
"""

import json
import os
from pathlib import Path

# The default file is in the same directory as this module
default_file = Path(__file__).resolve().parent / "leaderboard.json"

# Variable for the maximum length of a player name, used in add_score()
max_name_length = 20


def validate_entries(entry: object) -> bool:
    """
    Check if an entry is a valid leaderboard entry.
    Returns bool, True if the entry is a dict with a string 'name' that is not empty and less than max_name length
    and a numeric 'time' that is positive.
    """
    if isinstance(entry, dict):
        valid_name = (isinstance(entry.get("name"), str) and 0 < len(entry["name"]) <= max_name_length)
        valid_time = (isinstance(entry.get("time"), (int, float)) and entry["time"] >= 0)

        if valid_name and valid_time:
            return True

    return False


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
    valid_entries = [entry for entry in entries if validate_entries(entry)]

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

    if not temp_path.exists():
        raise OSError("Failed to save entries.")

    # Replace the original file with the temporary file
    else:
        os.replace(temp_path, path)


def add_score(name: str, seconds: int, filename: Path | str | None = None) -> bool:
    """
    Record a score.
    Raises ValueError for a blank name, name longer than max_name_length, or negative time.
    Returns True if the score was added successfully.
    """
    plr_name = name.strip()

    if not plr_name:
        raise ValueError("Player name cannot be blank.")

    if len(plr_name) > max_name_length:
        raise ValueError(f"Player name cannot be longer than {max_name_length} characters.")

    if seconds < 0:
        raise ValueError("Score cannot be negative.")

    entries = load(filename)
    entries.append({"name": plr_name, "time": seconds})
    save(entries, filename)
    return True


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
