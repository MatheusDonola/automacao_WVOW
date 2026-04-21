import pyautogui
import time
import random
from pynput import mouse
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

def capture_click_position(logger=None):
    clicked_position = {"x": None, "y": None}

    def on_click(x, y, button, pressed):
        if pressed:
            clicked_position["x"] = x
            clicked_position["y"] = y

            if logger:
                logger.log(f"Clique capturado em x={x}, y={y}")
            else:
                print(f"Clique capturado em x={x}, y={y}")

            return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    return clicked_position["x"], clicked_position["y"]

import re

def save_drag_to_config(config_key, end_x, end_y, duration=0.5, config_path="config.py"):
    with open(config_path, "r", encoding="utf-8") as file:
        content = file.read()

    new_block = f'''{config_key} = {{
    "end_x": {end_x},
    "end_y": {end_y},
    "duration": {duration}
}}'''

    pattern = rf"{config_key}\s*=\s*\{{.*?\}}"

    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, new_block, content, flags=re.DOTALL)
    else:
        content += f"\n\n{new_block}\n"

    with open(config_path, "w", encoding="utf-8") as file:
        file.write(content)

def capture_and_save_drag(config_key, duration=0.5, config_path="config.py", logger=None):
    if logger:
        logger.log(f"Click on the spawn spot {config_key}...")
    else:
        print(f"Click on the spawn spot {config_key}...")

    end_x, end_y = capture_click_position(logger=logger)
    save_drag_to_config(config_key, end_x, end_y, duration=duration, config_path=config_path)

    if logger:
        logger.log(f"{config_key} Success on saving coordinates: x={end_x}, y={end_y}")
    else:
        print(f"{config_key} Success on saving coordinates: x={end_x}, y={end_y}")

    return end_x, end_y