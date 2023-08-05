import tkinter as tk
from abc import ABC


class EventExecuter(ABC):

    def __init__(
        self,
        target: tk.Variable | tk.Tk | tk.Widget,
    ):
        self._target = target
