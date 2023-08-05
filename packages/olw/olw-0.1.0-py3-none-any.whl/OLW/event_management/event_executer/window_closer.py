import tkinter as tk
from typing import Callable

from .event_executer import EventExecuter


class WindowCloser(EventExecuter):
    """Windowを閉じる

    Args:
        target (tk.Tk): 対象のウィンドウ
    """

    def __init__(self, target: tk.Tk):
        super().__init__(target)
        self._target: tk.Tk
        self._target.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.__quit_funcs: list[Callable] = []

    def register_quit_procedure(self, func: Callable):
        """ウィンドウ閉じる前の終了処理関数を登録する

        Args:
            func (Callable): 終了処理関数
        """
        self.__quit_funcs.append(func)

    def on_closing(self):
        """ウィンドウを閉じる"""
        for func in self.__quit_funcs:
            func()
        self._target.destroy()
