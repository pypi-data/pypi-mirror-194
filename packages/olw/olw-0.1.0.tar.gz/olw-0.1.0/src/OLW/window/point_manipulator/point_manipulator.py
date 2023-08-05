import tkinter as tk

from .point import Point
from .size import Size


class PointManipulator:
    """ウィンドウ表示位置の取得と設定機能を提供するクラス

    Args:
        target (tk.Tk): 参照・操作対象のウィンドウオブジェクト
    """

    def __init__(self, target: tk.Tk):
        self._target = target

    def __get_geometry(self) -> tuple[Size, Point]:
        """画面のサイズと位置情報を取得する

        Returns:
            Size: 画面サイズ
            Point: 画面の位置
        """
        geometry = self._target.geometry()
        size, x, y = geometry.split('+')
        point = Point(int(x), int(y))
        w, h = size.split('x')
        return Size(int(w), int(h)), point

    def get_point(self) -> Point:
        """現在の座標位置を返す

        Returns:
            Point: 現在の座標
        """
        _, point = self.__get_geometry()
        return point

    def set_point(self, x: int | None, y: int | None):
        """指定の表示位置に設定する

        Args:
            x (int | None): 指定するx座標位置.Noneだと現在値まま
            y (int | None): 指定するy座標位置.Noneだと現在値まま
        """
        if x is None and y is None:
            return
        current_point = self.get_point()
        new_point = current_point.copy()
        if x is not None:
            new_point.x = x
        if y is not None:
            new_point.y = y
        self._target.geometry(new_point.for_geometry())

    def set_point_as_Point(self, point: Point):
        """指定の表示位置に設定する

        Args:
            point (Point): 指定する座標位置
        """
        self.set_point(point.x, point.y)

    def get_size(self) -> Size:
        """現在のウィンドウサイズを取得する

        Returns:
            Size: 現在のウィンドウサイズ
        """
        size, _ = self.__get_geometry()
        return size
