import tkinter as tk
from datetime import datetime as dt
from datetime import timedelta as td

from ...window import Point, PointManipulator, Window
from ...window.events import MouseEvents
from .event_executer import EventExecuter


class WindowMover(EventExecuter):
    """ウィンドウを移動するイベントのクラス

    Args:
        target (tk.Tk): 移動対象のウィンドウオブジェクト
    """

    @classmethod
    def bind(cls, window: Window):
        """対象のWindowオブジェクトに移動イベントを紐付ける

        Args:
            window (Window): 対象のWindowオブジェクト
        """
        mover = cls(window.root)
        window.root.bind(MouseEvents.LeftClick, mover.on_drag_start)
        window.root.bind(MouseEvents.LeftDrag, mover.on_drag)

    def __init__(self, target: tk.Tk):
        super().__init__(target)
        self._target: tk.Tk
        self._manipulator = PointManipulator(target)
        self.__start_point: Point | None = None
        self.__last_update = dt.min

    @staticmethod
    def __get_current_point(event: tk.Event) -> Point:
        return Point(event.x, event.y)

    def __elapsed_time(self) -> bool:
        """既定時間を上回ったかどうか返す

        Returns:
            bool: True: 既定時間を超えた, False: 既定時間以内
        """
        now = dt.now()
        if now - self.__last_update > td(seconds=0.05):
            self.__last_update = now
            return True
        return False

    def on_drag_start(self, event: tk.Event):
        """ドラッグアンドドロップの開始時のハンドラ"""
        self.__start_point = self.__get_current_point(event)
        self.__last_update = dt.now()

    def on_drag(self, event: tk.Event):
        """ドラッグアンドドロップのドラッグ中のハンドラ"""
        if not self.__elapsed_time():
            return
        if self.__start_point is None:
            raise ValueError('unset start point')
        current_point = self.__get_current_point(event)
        xdiff = current_point.x - self.__start_point.x
        ydiff = current_point.y - self.__start_point.y
        new_point = self._manipulator.get_point()
        new_point.offset(x=xdiff, y=ydiff)
        self._manipulator.set_point_as_Point(new_point)
