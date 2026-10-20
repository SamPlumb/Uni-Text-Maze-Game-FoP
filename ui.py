"""
KeyError: The Keeper of the Golden Key
ui.py

User Interface for the game:
display boxes, menus, and prompts.
"""
import re
from shutil import get_terminal_size
from textwrap import wrap
from time import sleep

left, right, center = "<", ">", "^"
menu_time_delay: float = 0.5  # Delay in seconds for menu transitions
max_line_length = 150  # Maximum line length for display boxes
divider = "-" * 30

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
bold_start, bold_end = "\033[1m", "\033[0m"


def bold(text: str) -> str:
    """
    Return text wrapped in ANSI bold codes.
    """
    return f"{bold_start}{text}{bold_end}"


def visible_len(text: str) -> int:
    """
    Return the length of text as displayed, ignoring ANSI escape codes.
    """
    return len(ansi_escape.sub('', text))


def pad_visible(text: str, width: int, align: str = center) -> str:
    """
    Pad visible text to a given width without counting ANSI escape codes.
    """
    length = visible_len(text)
    if length >= width:
        return text

    pad = width - length
    if align == left:
        return f"{text}{' ' * pad}"
    if align == right:
        return f"{' ' * pad}{text}"

    left_pad = pad // 2
    right_pad = pad - left_pad
    return f"{' ' * left_pad}{text}{' ' * right_pad}"


def menu_delay(delay: float | None = None) -> None:
    """Pause briefly so menus don't flood the screen faster than they can be read."""
    sleep(menu_time_delay if delay is None else delay)


def wrap_line(line: str, width: int) -> list[str]:
    """
    Wrap a line to a given width without breaking ANSI escape codes.
    A line that is entirely bold stays bold after wrapping.
    """
    if visible_len(line) <= width:
        return [line]

    pieces = wrap(ansi_escape.sub('', line), width=width)

    if line.startswith(bold_start) and line.endswith(bold_end):
        return [bold(piece) for piece in pieces]

    return pieces


def d_box(text: list[str], align: str = center) -> None:
    """
    Print lines of text inside a box that fits the terminal, centered on screen.
    Long lines are wrapped.
    Align justification is left, right or center and applies to the text within the box.
    Raises ValueError for an empty or non-string list or bad alignment.
    """
    if align not in (left, right, center):
        raise ValueError("Alignment must be left, right or center.")

    if not text or not isinstance(text, list) or not all(isinstance(line, str) for line in text):
        raise ValueError("Text must be a non-empty list of strings.")

    terminal_width = get_terminal_size().columns
    max_width = min(max(visible_len(line) for line in text) + 4,
                    terminal_width - 6,
                    max_line_length)

    lines: list[str] = []

    for line in text:
        lines.extend(wrap_line(line, max_width - 4))

    inner_width = max(visible_len(line) for line in lines) + 2
    left_margin = " " * max(0, (terminal_width - inner_width - 2) // 2)

    print(f"{left_margin}╔{'═' * (inner_width + 2)}╗")

    for line in lines:
        formatted_line = f" {pad_visible(line, inner_width, align)} "
        print(f"{left_margin}║{formatted_line}║")

    print(f"{left_margin}╚{'═' * (inner_width + 2)}╝")


def show_menu(text: list[str], align: str = center, delay: float = menu_time_delay) -> None:
    """
    Show a menu with a brief delay.
    """
    menu_delay(delay)
    d_box(text, align)
