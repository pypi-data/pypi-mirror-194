from ..window import Window
from .event_connector import TopmostSwitchEvent, WindowCloseEvent
from .event_executer import (DateObserver, TimeCounter, TimeObserver, WindowMover)


class EventFactory:
    """イベントハンドラと各オブジェクトの紐づけを行う"""

    @staticmethod
    def create(window: Window):
        # 定期実行イベント設定
        counter = TimeCounter()
        observer = TimeObserver(window.timevar)
        counter.add_observer(observer)
        observer = DateObserver(window.datevar)
        counter.add_observer(observer)
        WindowMover.bind(window)

        # コンテキストメニューのイベント設定
        TopmostSwitchEvent.bind(window)
        WindowCloseEvent.bind(window, counter.quit)
