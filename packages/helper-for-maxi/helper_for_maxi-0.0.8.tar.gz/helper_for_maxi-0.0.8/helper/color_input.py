from .terminal import Terminal

def color_input(text: str = None, beforeColor: Terminal.color.foreground = None):
    r"""Gets an input

    Prints the given text in cyan and changes the color back to beforeColor

    Parameters
    ----------
    text: Optional[:class:`str`]
        The text that is printed before getting the input
        DEFAULT: None
    beforeColor: Optional[:class:`Terminal.color.foreground`]
        The color that was used before (if u want it to change back)
        DEFAULT: None
    """
    if text is not None:
        res = input(Terminal.color.foreground.FCYAN + text)
    else:
        res = input(Terminal.color.foreground.FCYAN)
    if beforeColor is not None:
        print(beforeColor)
    return res