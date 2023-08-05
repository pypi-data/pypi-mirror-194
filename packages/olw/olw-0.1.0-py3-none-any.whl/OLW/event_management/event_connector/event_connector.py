import tkinter as tk
from abc import ABC, abstractmethod
from typing import Type

from ...window import Window
from ..event_executer import EventExecuter


class EventConnector(ABC):
    """コンテキストメニューとイベントを紐付ける基底クラス

    Args:
        menu (tk.Menu): コンテキストメニューのオブジェクト
        event (EventExecuter): 紐付けるイベントの処理を持つオブジェクト
    """

    @classmethod
    @abstractmethod
    def bind(cls, window: Window, executer_class: Type[EventExecuter]):
        cls(window.menu, executer_class(window.root))

    def __init__(self, menu: tk.Menu, event: EventExecuter):
        self._master = menu
        self._executer = event
        self._index: int = 0
        self._register_menu()

    def _register_menu(self):
        """コンテキストメニューにタイトルバー表示切り替えを追加する

        Raises:
            ValueError: 想定外のラベルが設定されている時
        """
        msg = self._select_msg()
        self._master.add_command(label=msg, command=self.event)
        index = self._master.index(msg)
        if index is None:
            raise ValueError
        self._index = index

    @abstractmethod
    def _select_msg(self) -> str:
        """現在の表示状態に対応したラベル文字列を返す

        Returns:
            str: メニューに表示するラベル文字列
        """
        ...

    @abstractmethod
    def event(self):
        """タイトルバー表示切替イベントのハンドラ"""
        ...
