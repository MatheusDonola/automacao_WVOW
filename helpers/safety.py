import random
import time
import pyautogui

from helpers.screen import find_exists


def click_right_corner(margin=40, sleep_after=0.25):
    sw, sh = pyautogui.size()

    x = random.randint(sw - margin, sw - 5)
    y = random.randint(5, margin)

    pyautogui.click(x, y)
    time.sleep(sleep_after)


def serverc_safety(stop_event=None):
    if stop_event is not None and stop_event.is_set():
        return

    found = find_exists(
        "serverc.png",
        region_key="serverc",
        start_conf=0.80,
        min_conf=0.50,
        pasta="safe"
    )

    if stop_event is not None and stop_event.is_set():
        return

    if found:
        click_right_corner()