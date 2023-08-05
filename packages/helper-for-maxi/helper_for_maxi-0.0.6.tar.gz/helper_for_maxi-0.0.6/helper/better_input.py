from .better_print import better_print as BetterPrint


def better_input(text: str, end: str = None, delay: float = None):
    r"""Gets an input

    Prints the given text letter by letter using the specified delay and gets an input() after

    Parameters
    ----------
    text: :class:`str`
        The text that is printed letter by letter
    
    end: Optional[:class:`str`]
        The text that is passed into the :func:`input()` statement. 
        Be aware that this part is not printed letter by letter.
        DEFAULT: None

    delay: Optional[:class:`float`]
        Changes the time between each printed letter
        DEFAULT: None
    """
    
    if delay is not None:
        BetterPrint(text, delay)
    else:
        BetterPrint(text)
    if end is not None:
        res = input(end)
    else:
        res = input()
    return res