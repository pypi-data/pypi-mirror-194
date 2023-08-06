###############################################################################
# Rudimentary Progress Bar Implementation
###############################################################################
###############################################################################
# Imports
###############################################################################
import os
import sys

from time import perf_counter
from typing import Any, Iterable, Sized, TextIO


###############################################################################
# Terminal Colors
#     >>> CYAN = "\033[96m"; RESET = "\033[0m"
#     >>> print("Hello " + CYAN + "World" + RESET + "!")
#     Hello World!
#
# Above, ("Hello ", "!") will be in the current color, "World" will be cyan.
###############################################################################
# Windows, apparently.
# See SO question: "287871/how-do-i-print-colored-text-to-the-terminal".
os.system("")

CYAN = "\033[96m"
RESET = "\033[0m"


###############################################################################
# Helpers
###############################################################################
def format_duration(duration: float) -> str:
    """
    Formats a duration in seconds as a clock time string of the form MM:SS,
    where MM is the number of minutes and SS is the number of seconds with two
    decimal places.
    """
    minutes, seconds = int(duration // 60), duration % 60
    return f"{minutes:02d}:{seconds:05.2f}"


###############################################################################
# Progress Bar Utility
###############################################################################
def progress(iterable: Iterable[Any], iterations: int | None = None,
             prefix: str | None = None, min_interval: float = 0.1,
             file: TextIO = sys.stdout, keep: bool = True) -> Iterable[Any]:
    """
    Displays a progress bar and updates it for each item in the iterable.

    Args:
        iterable:
            An iterable to track the progress of.
        iterations:
            The number of iterations. If `None`, tries `len(iterable)`.
        prefix:
            A string to prepend to the progress bar. If `None`, sets prefix to
            "Progress: ".
        min_interval:
            Minimum time interval between updates in seconds.
        file:
            File to write the progress bar to. Defaults to `sys.stdout`.
        keep:
            If `True` (the default) and the file is connected to a terminal,
            continually update the progress bar on the same line. Otherwise,
            each time there is an update, a progress bar will be written on
            a new line.

    Raises:
        ValueError:
            If `iterations` is not supplied and the number of iterations could
            not be determined.

    Yields:
        The items in the iterable.
    """
    if iterations is None:
        if isinstance(iterable, Sized):
            iterations = len(iterable)
        else:
            raise ValueError("Can't determine the number of iterations")

    if prefix is None:
        prefix = "Progress: "

    START_TIME = perf_counter()
    last_update_time = START_TIME

    # Number of completed iterations.
    k = 0

    # Get the terminal width. Assume terminal width remains unchanged.
    try:
        TERMINAL_WIDTH, _ = os.get_terminal_size(file.fileno())
        end = "\r" if keep else "\n"
    except Exception:
        TERMINAL_WIDTH = 80
        end = "\n"

    MAX_CHARS = TERMINAL_WIDTH + len(CYAN) + len(RESET)

    for item in iterable:
        yield item
        k += 1

        current_time = perf_counter()

        if current_time - last_update_time < min_interval:
            continue

        last_update_time = current_time

        elapsed = current_time - START_TIME
        # Iterations (completed) per second.
        rate_fmt = f"{k / elapsed:.2f} it/s"
        # Time elapsed as a clock time string (MM:SS).
        time_fmt = format_duration(elapsed)

        # Length of the progress bar as a function of the terminal width.
        max_bar_length = TERMINAL_WIDTH - \
            len(f"{prefix}[] {k}/{iterations} ({rate_fmt}, {time_fmt})")

        if max_bar_length > 0:
            filled_length = (max_bar_length * k) // iterations
            bar = f"{'=' * filled_length}" \
                  f"{'-' * (max_bar_length - filled_length)}"
        else:
            # Technically, this is not needed.
            bar = ""

        progress_bar = f"{prefix}[{CYAN}{bar}{RESET}] " \
                       f"{k}/{iterations} ({rate_fmt}, {time_fmt})"
        print(progress_bar[:MAX_CHARS], end=end, file=file, flush=True)

    if keep:
        print("\n", file=file)
    else:
        print(file=file)
