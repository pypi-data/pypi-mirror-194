from abc import ABC, abstractmethod
from datetime import datetime as dt
from threading import Thread

from ..observer import WatchObserver


class WatchCounter(ABC):
    """時刻カウンタの基底クラス"""

    def __init__(self):
        self.__observers: list[WatchObserver] = []
        self._quit_loop = False
        self.__thread = Thread(target=self._count, name='continue_count')
        self.__thread.start()

    def add_observer(self, observer: WatchObserver):
        """オブザーバーを追加する

        Args:
            observer (WatchObserver): 追加するオブザーバー
        """
        self.__observers.append(observer)

    def _notify_observer(self, datetime: dt):
        """全オブザーバーに通知を送る

        Args:
            datetime (dt): 通知する時刻情報
        """
        for observer in self.__observers:
            observer.update(datetime)

    @abstractmethod
    def _count(self):
        """カウントを実施する"""
        ...

    def quit(self):
        """スレッドを停止する"""
        self._quit_loop = True
        self.__thread.join()
