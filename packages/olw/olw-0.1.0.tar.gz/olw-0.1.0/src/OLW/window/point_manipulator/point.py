from dataclasses import dataclass
from typing import TypeVar

T = TypeVar('T', bound='Point')


@dataclass
class Point:
    """画面の座標を扱う値オブジェクト

    Attributes:
        x (int): x座標
        y (int): y座標
    """
    x: int
    y: int

    def offset(self, *, x: int | None = None, y: int | None = None):
        """座標位置を指定した分ずらす

        Args:
            x (int | None, optional): x座標のオフセット量. Defaults to None.
            y (int | None, optional): y座標のオフセット量. Defaults to None.
        """
        if x is not None:
            self.x += x
        if y is not None:
            self.y += y

    def for_geometry(self) -> str:
        """tkのgeometry設定向けの文字列にして返す

        Returns:
            str: geometryに渡す座標系フォーマットの文字列
        """
        return f'+{self.x}+{self.y}'

    def copy(self: T) -> T:
        """値の全く同じ別の座標インスタンスを生成して返す

        Args:
            self (Point): 生成した新しい座標インスタンス

        Returns:
            T: _description_
        """
        return self.__class__(self.x, self.y)
