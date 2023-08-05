from datetime import datetime as dt
from time import sleep

from .watch_counter import WatchCounter


class TimeCounter(WatchCounter):
    """時刻を定期的に確認して各オブザーバーに通知する"""

    def _count(self):
        """定期的に現在時刻を取得して通知する"""
        while not self._quit_loop:
            self._notify_observer(dt.now())
            sleep(0.2)
