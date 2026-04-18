import pyautogui
import time
import random
from pynput.mouse import Listener, mouse
from helpers import logger
from config import REGIONS, COORDS

def click_search_center(delay_before=0.5, jitter=6):
    time.sleep(delay_before)

    base_x = 612
    base_y = 749

    x = base_x + random.randint(-jitter, jitter)
    y = base_y + random.randint(-jitter, jitter)

    pyautogui.click(x, y)
    time.sleep(0.2)


def click_region(region_key, margin=8, sleep_after=0.15):
    if region_key not in REGIONS:
        return False

    x, y, w, h = REGIONS[region_key]

    rx = random.randint(x + margin, x + w - margin)
    ry = random.randint(y + margin, y + h - margin)

    pyautogui.click(rx, ry)
    time.sleep(sleep_after)
    return True


def click_lizard_center(delay_before=0.5, jitter=8):
    time.sleep(delay_before)

    base_x, base_y = COORDS["LIZARD_CENTER"]

    x = base_x + random.randint(-jitter, jitter)
    y = base_y + random.randint(-jitter, jitter)

    pyautogui.click(x, y)
    time.sleep(0.1)

def click_rebel_center(delay_before=0.5, jitter=8):
    time.sleep(delay_before)

    base_x, base_y = COORDS["REBEL"]

    x = base_x + random.randint(-jitter, jitter)
    y = base_y + random.randint(-jitter, jitter)

    pyautogui.click(x, y)
    time.sleep(0.1)

def capture_click_position():
    clicked_position = {"x": None, "y": None}

    def on_click(x, y, button, pressed):
        if pressed:
            clicked_position["x"] = x
            clicked_position["y"] = y
            logger.log(f"Clique capturado em x={x}, y={y}")
            return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    return clicked_position["x"], clicked_position["y"]