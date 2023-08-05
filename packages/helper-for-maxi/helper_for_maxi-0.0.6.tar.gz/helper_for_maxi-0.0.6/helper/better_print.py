import sys
import time


def better_print(text: str, delay: float = .1):
    r"""Prints text

    Prints the given text letter by letter to the command line using the specified delay

    Parameters
    ----------
    text: :class:`str`
        The text that is printed letter by letter

    delay: Optional[:class:`float`]
        Changes the time between each printed letter
        DEFAULT: .1
    """

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)