import random
import time
import pyautogui

from helpers.screen import find_exists
from helpers.logger import log



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

def connection_reset(stop_event):
    for tentativa in range(50):
        if stop_event.is_set():
            return False

        if not find_exists(
            "reload.png",
            region_key="RESET",
            start_conf=0.7,
            min_conf=0.6,
            step=0.05,
            retry_delay=0.2,
            pasta="reload"
        ):
            return False

        log(f"Game disconected, trying to reconect... try {tentativa + 1}")
        pyautogui.click(x=944, y=671)
        time.sleep(2)
        pyautogui.click(x=951, y=796)
        time.sleep(2)
        if not find_exists(
            "reload.png",
            region_key="RESET",
            start_conf=0.7,
            min_conf=0.6,
            step=0.05,
            retry_delay=0.2,
            pasta="reload"
        ):
                pyautogui.click(x=940, y=958)
                time.sleep(20)
                pyautogui.click(x=1623, y=303)
                time.sleep(1)
                pyautogui.click(x=134, y=958)

                log("succes on reconection")
            
                return True


    return False