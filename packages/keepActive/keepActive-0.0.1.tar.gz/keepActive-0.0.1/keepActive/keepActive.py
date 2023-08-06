
import pyautogui
import threading
import time

class keepActive:
    flag = False

    @classmethod
    def start(cls, time_in_minutes=None):
        cls.flag = True
        if time_in_minutes is None:
            threading.Thread(target=cls._keep_active_forever).start()
        else:
            threading.Thread(target=cls._keep_active_for_time, args=(time_in_minutes,)).start()

    @classmethod
    def stop(cls):
        cls.flag = False

    @classmethod
    def _keep_active_forever(cls):
        while cls.flag:
            pyautogui.press("f20")
            time.sleep(30)

    @classmethod
    def _keep_active_for_time(cls, time_in_minutes):
        end_time = time.time() + time_in_minutes * 60
        while cls.flag and time.time() < end_time:
            pyautogui.press("f20")
            time.sleep(30)