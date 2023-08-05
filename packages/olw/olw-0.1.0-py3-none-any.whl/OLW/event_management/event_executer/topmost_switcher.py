import tkinter as tk

from .event_executer import EventExecuter


class TopmostSwitcher(EventExecuter):
    """ウィンドウの最前面表示を切り替える

    Args:
        target (tk.Tk): 対象のウィンドウ
    """

    def __init__(self, target: tk.Tk):
        super().__init__(target)
        self._target: tk.Tk
        # NOTE: attribute直読だと反映が遅れるっぽいので別管理フラグを用意する
        self.__status = bool(target.attributes('-topmost'))

    def is_topmost(self) -> bool:
        """現在の設定状態を返す

        Returns:
            bool: True: 最前面固定中, False: 最前面固定解除
        """
        return self.__status

    def keep(self):
        """最前面固定にする"""
        self.__switch(True)

    def release(self):
        """最前面固定を解除する"""
        self.__switch(False)

    def __switch(self, mode: bool):
        """最前面固定を切り替える

        Args:
            mode (bool): True: 固定する, False: 解除する
        """
        self.__status = mode
        self._target.attributes("-topmost", mode)
