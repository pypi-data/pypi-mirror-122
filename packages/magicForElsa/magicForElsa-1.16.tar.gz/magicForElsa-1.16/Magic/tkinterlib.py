"""
This  module is for stylising the Tkinter GUI
"""
from functools import partial
from tkinter import Button

from Magic import theme

bg_colour, text_color, button_colour = theme.read_theme()


def tkinter_initialise(a, x=0, y=0, top=1, noborders=True, opacity=0.9):
    """[Used to mordernify tkinter gui boxes]

    Args:
        a ([type]): [The root name of the gui]
        x (int, optional): [x-coordinate to place the box ]. Defaults to 0.
        y (int, optional): [y-coordinate to place the box ]. Defaults to 0.
        top (int, optional): [1 if the GUI should always be on the top of other windows..else 0]. Defaults to 1.
        no-borders (bool, optional): [True if no need of borders..else False]. Defaults to True.
        opacity (float, optional): [opacity ranges from 0 to 1. 0 being complete transparent]. Defaults to 0.9.
    """

    a.withdraw()  # Hide tkinter windows to finish initialization
    a.attributes("-alpha", opacity)  # Opacity of tkinter window
    a.overrideredirect(noborders)  # Remove Borders and default title bars
    a.configure(bg=bg_colour)
    a.attributes(
        "-topmost", top
    )  # Decides if the tkinter windows shld always be on the top of other window
    a.geometry(f"+{x}+{y}")  # positions tkinter windows at x and y coordinate

    a.deiconify()  # show the tkinter window back


def on_enter(event, but):
    """[Part of hover effect for buttons]

    Args:
        event ([type]): [not imp]
        but ([type]): [Button which shld have the effect ]
    """
    # Change the button colour from background colour to button colour fo hover effect when mouse enters the button field

    but.config(bg=button_colour)
    but.config(fg=bg_colour)


def on_leave(event, but):
    """[Part of hover effect for buttons]

    Args:
        event ([type]): [not imp]
        but ([type]): [Button which shld have the effect ]
    """
    # Change back the button colour to background colour when mouse leaves the button field.

    but.config(bg=bg_colour)
    but.config(fg=text_color)


def TButton(root, text="", command=None, relief='ridge'):
    b = Button(root,
               text=text,
               fg=text_color,
               bd=0,
               bg=bg_colour,
               command=command,
               relief=relief)
    b.bind("<Enter>", partial(on_enter, but=b))
    b.bind("<Leave>", partial(on_leave, but=b))

    return b
