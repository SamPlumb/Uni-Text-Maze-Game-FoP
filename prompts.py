"""
KeyError: The Keeper of the Golden Key
prompts.py

User input prompts:
Reads and validates player inputs
"""
from leaderboard import validate_player_name, clean_name
from ui import show_menu, bold, divider


def enter_choice_prompt(num_options: int) -> str:
    """
    Prompt the user to enter a choice.
    """
    return f"Please enter your choice (1-{num_options}):"


def invalid_choice_menu(user_input: str, num_choices: int) -> None:
    """
    Display a message for an invalid menu choice.
    """
    show_menu([
        bold(f"Invalid choice: '{user_input}'."),
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
        invalid_choice_menu(user_choice, num_choices)


def invalid_name_menu(name: str, error: str) -> None:
    """
    Display a message for an invalid player name.
    """
    show_menu([
        bold(f"Invalid name: '{name}'."),
        divider,
        error,
        "Please enter a valid name:"])


def prompt_name() -> str:
    """
    Prompt the user for a name and validate the input.
    Returns the valid name as a string.
    """
    while True:
        name = clean_name(input())
        error = validate_player_name(name)

        if error is None:
            return name

        invalid_name_menu(name, error)
