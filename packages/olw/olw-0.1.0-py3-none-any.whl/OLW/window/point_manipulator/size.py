from dataclasses import dataclass
from typing import TypeVar

T = TypeVar('T', bound='Size')


@dataclass
class Size:
    """画面の大きさを扱う値オブジェクト

    Attributes:
        width (int): 画面幅
        height (int): 画面高さ
    """
    width: int
    height: int

    def for_geometry(self) -> str:
        """tkのgeometry設定向けの文字列にして返す

        Returns:
            str: geometryに渡す座標系フォーマットの文字列
        """
        return f'{self.width}x{self.height}'

    def copy(self: T) -> T:
        """値の全く同じ別の座標インスタンスを生成して返す

        Args:
            self (Point): 生成した新しい座標インスタンス

        Returns:
            T: _description_
        """
        return self.__class__(self.width, self.height)
