import tkinter as tk
from abc import ABC, abstractmethod
from datetime import datetime as dt

from ..event_executer import EventExecuter


class WatchObserver(EventExecuter, ABC):
    """時刻の更新を通知するオブザーバーの基底クラス

    Args:
        target (tk.StringVar): 更新対象のオブジェクト
    """

    def __init__(self, target: tk.StringVar):
        super().__init__(target)
        self._target: tk.StringVar
        self._last_time = dt.min

    @abstractmethod
    def update(self, datetime: dt):
        """時刻系の更新処理を実施する

        Args:
            datetime (dt): 更新する時刻情報
        """
        self._last_time = datetime
