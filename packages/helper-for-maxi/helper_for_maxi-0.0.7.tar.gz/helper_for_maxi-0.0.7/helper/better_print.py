import time


def better_print(text: str, delay: float = .01):
    r"""Prints text

    Prints the given text letter by letter to the command line using the specified delay

    Parameters
    ----------
    text: :class:`str`
        The text that is printed letter by letter

    delay: Optional[:class:`float`]
        Changes the time between each printed letter
        DEFAULT: .01
    """
    
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print('')