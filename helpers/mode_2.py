from helpers.screen import find_and_click
from helpers.safety import serverc_safety
from helpers.screen import find_image
from helpers.logger import log
import pyautogui
import time

def mode_2(stop_event):
    if stop_event.is_set():
        return
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
    
    pyautogui.moveTo(x=945, y=515)
    pyautogui.dragTo(1111, 415, 0.6, button="left")
    find_and_click("summoner2.png", pasta="mode_2", confidence=0.8)
    pyautogui.click(1111, 415)
    time.sleep(0.2)
    find_and_click("rally.png", pasta="mode_2", confidence=0.8)
    time.sleep(0.1)
    find_and_click("march.png", region_key="march", confidence=0.30, tries=5)
    time.sleep(0.5)