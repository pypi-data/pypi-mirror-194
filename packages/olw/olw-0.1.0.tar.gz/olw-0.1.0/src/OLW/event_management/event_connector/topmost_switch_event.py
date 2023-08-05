import tkinter as tk

from ...window import Window
from ..event_executer import TopmostSwitcher
from .event_connector import EventConnector


class TopmostSwitchEvent(EventConnector):
    """最前面表示固定切り替えイベントを画面オブジェクトと紐付ける

    Args:
        menu (tk.Menu): コンテキストメニューのオブジェクト
        event (TopmostSwitcher): 最前面表示固定切り替えオブジェクト
    """

    @classmethod
    def bind(cls, window: Window):
        """指定のWindowのコンテキストメニューに最前面固定切り替えイベントを設定する

        Args:
            window (Window): 設定対象のウィンドウオブジェクト
        """
        super().bind(window, TopmostSwitcher)

    def __init__(self, menu: tk.Menu, event: TopmostSwitcher):
        super().__init__(menu, event)
        self._executer: TopmostSwitcher

    def _select_msg(self) -> str:
        if self._executer.is_topmost():
            return '最前面固定を解除'
        else:
            return '最前面に固定する'

    def event(self):
        if self._executer.is_topmost():
            self._executer.release()
        else:
            self._executer.keep()
        new_msg = self._select_msg()
        self._master.entryconfigure(self._index, label=new_msg)
