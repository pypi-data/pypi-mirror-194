import tkinter as tk
from typing import Callable, Iterable

from ...window import Window
from ..event_executer import WindowCloser
from .event_connector import EventConnector


class WindowCloseEvent(EventConnector):
    """ウィンドウを閉じるイベントを画面オブジェクトと紐付ける

    Args:
        menu (tk.Menu): コンテキストメニューのオブジェクト
        event (WindowCloser): ウィンドウを閉じるイベント実行オブジェクト
    """

    @classmethod
    def bind(cls, window: Window, functions: Iterable[Callable] | Callable):
        """指定のWindowのコンテキストメニューに閉じるイベントを設定する

        Args:
            window (Window): 設定対象のウィンドウオブジェクト
        """
        executer = WindowCloser(window.root)
        if not isinstance(functions, Iterable):
            functions = [functions]
        for func in functions:
            executer.register_quit_procedure(func)
        WindowCloseEvent(window.menu, executer)

    def __init__(self, menu: tk.Menu, event: WindowCloser):
        super().__init__(menu, event)
        self._executer: WindowCloser

    def _select_msg(self) -> str:
        return "閉じる"

    def event(self):
        self._executer.on_closing()
