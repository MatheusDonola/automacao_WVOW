from helpers.screen import find_and_click
from helpers.safety import serverc_safety
from helpers.screen import find_image
from helpers.logger import log
from helpers.flow import verify_and_execute, verify_crash
from helpers.timers import executar_reset_geral
from config import MODE_2_DRAG
import pyautogui
import time
from core.statistics import STATS

def mode_2(stop_event):
    if stop_event.is_set():
        return
    verify_crash()
    verify_and_execute()

    if not find_and_click(
        "events.png",
        region_key="events",
        confidence=0.75,
        tries=5,
        retry_delay=0.2,
        jitter=2,
        pasta="mode_2"):
        return

    if stop_event.is_set():
        return
    
    time.sleep(0.1)
    
    if not find_and_click(
    "tower.png",
    region_key="tower",
    confidence=0.75,
    tries=5,
    retry_delay=0.2,
    jitter=2,
    pasta="mode_2"):
        return
    
    time.sleep(0.1)

    if not find_and_click(
    "summoner.png",
    region_key="summoner",
    confidence=0.85,
    tries=5,
    retry_delay=0.2,
    jitter=2,
    pasta="mode_2"):
        return
    
    if verify_error():
        return
    pyautogui.moveTo(x=945, y=515)
    pyautogui.dragTo(
        MODE_2_DRAG["end_x"],
        MODE_2_DRAG["end_y"],
        MODE_2_DRAG["duration"],
        button="left"
    )
    find_and_click("summoner2.png", pasta="mode_2", confidence=0.8)
    pyautogui.click(x=MODE_2_DRAG["end_x"], y=MODE_2_DRAG["end_y"])
    time.sleep(0.2)
    find_and_click("rally.png", pasta="mode_2", confidence=0.8)
    time.sleep(0.1)
    if find_and_click("march.png", region_key="march", confidence=0.30, tries=5):
        STATS.tower_siege += 1
    time.sleep(0.5)
    if verify_error():
        return

def verify_error():
    if find_and_click(
    "error.png",
    region_key="error",
    confidence=0.85,
    tries=1,
    retry_delay=0.2,
    jitter=2,
    pasta="mode_2"):
        pyautogui.click(1408, 237)
        executar_reset_geral()
        return True
    
    else:
        return False

