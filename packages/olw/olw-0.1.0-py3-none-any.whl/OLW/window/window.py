from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

from .events import MouseEvents


class Window:
    """時計ウィンドウのオブジェクトセット

    Args:
        root (tk.Tk): ウィンドウルート
        menu (tk.Menu): コンテキストメニュー
        frame (ttk.Frame): オブジェクト配置フレーム
        time (ttk.Label): 時刻表示ラベル
        timevar (tk.StringVar): 時刻表示値更新用変数
        date (ttk.Label): 日付表示ラベル
        datevar (tk.StringVar): 日付表示値更新用変数
    """

    @classmethod
    def create(cls) -> Window:
        # ウィンドウルート設定
        root = tk.Tk()
        root.title('Resident watch')
        root.geometry('300x100')
        root.minsize(300, 80)
        root.overrideredirect(True)
        root.update()

        # コンテキストメニュー追加
        menu = tk.Menu(root, tearoff=0)
        root.bind(MouseEvents.RightClick, lambda e: menu.post(e.x_root, e.y_root))

        # ウィンドウフレーム配置
        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH)

        # 時刻ラベル配置
        t_font = tkfont.Font(family="M+ 1mn", size=34, weight='bold')
        t_var = tk.StringVar(frame)
        time = ttk.Label(frame, textvariable=t_var, font=t_font, anchor='center')
        time.pack(fill=tk.BOTH, expand=True, pady=(5, 0), padx=10)

        # 日付ラベル配置
        d_font = tkfont.Font(family="M+ 1mn", size=12)
        d_var = tk.StringVar(frame)
        date = ttk.Label(frame, textvariable=d_var, font=d_font, anchor='center')
        date.pack(fill=tk.BOTH, expand=True, pady=(0, 5), padx=10)

        return cls(root, menu, frame, time, t_var, date, d_var)

    def __init__(
        self,
        root: tk.Tk,
        menu: tk.Menu,
        frame: ttk.Frame,
        time: ttk.Label,
        timevar: tk.StringVar,
        date: ttk.Label,
        datevar: tk.StringVar,
    ):
        self.__root = root
        self.__menu = menu
        self.__frame = frame
        self.__time = time
        self.__timevar = timevar
        self.__date = date
        self.__datevar = datevar

    @property
    def root(self) -> tk.Tk:
        return self.__root

    @property
    def menu(self) -> tk.Menu:
        return self.__menu

    @property
    def frame(self) -> ttk.Frame:
        return self.__frame

    @property
    def time(self) -> ttk.Label:
        return self.__time

    @property
    def timevar(self) -> tk.StringVar:
        return self.__timevar

    @property
    def date(self) -> ttk.Label:
        return self.__date

    @property
    def datevar(self) -> tk.StringVar:
        return self.__datevar

    def run(self):
        """ウィンドウを表示する"""
        self.__root.mainloop()
