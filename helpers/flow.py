import pyautogui
import time
import config

from helpers.screen import find_and_click, check_error
from helpers.clicks import click_lizard_center, click_search_center, click_rebel_center
from helpers.paths import img_path
from helpers.screen import find_exists, check_error
from helpers.clicks import click_region
from core.statistics import STATS
from helpers.logger import log, debug
import config

from helpers.paths import cmd_path
from datetime import datetime

DEBUG_CMD = False
FIRELIZARD = config.FIRELIZARD

def sleep_speed2(delay):
    if config.SPEED_MODE == "SLOW":
        time.sleep(delay * 3)
    elif config.SPEED_MODE == "NORMAL":
        time.sleep(delay)
    elif config.SPEED_MODE == "FAST":
        time.sleep(delay * 0.1)
    else:
        time.sleep(delay)

def mainfuct():
    if not find_exists("lupa.png", region_key="lupa", start_conf=0.5, min_conf=0.3):
        check_error()
        return False

    click_region("lupa_click")

    sleep_speed2(0.3)

    if FIRELIZARD:
        if not find_and_click("firelizard.png", region_key="firelizard", confidence=0.7, tries=5):
            return False

    if not find_and_click("search.png", region_key="search", confidence=0.5, tries=5):
        return False
        
    time.sleep(2.3)

    if FIRELIZARD:
        click_lizard_center(delay_before=0.6, jitter=7)
    else:
        click_rebel_center(delay_before=0.5, jitter=8)

    #time.sleep(0.2)
    sleep_speed2(0.2)
  
    if FIRELIZARD:
        if not find_and_click(
            "rally.png",
            region_key="rally",
            confidence=0.45,
            tries=6,           
            retry_delay=0.15
        ):
            return False
    else:
        if not find_and_click("attk.png", region_key="attk", confidence=0.7, tries=5):
            return False
        
    sleep_speed2(0.2)

    if not find_and_click("march.png", region_key="march", confidence=0.30, tries=5):
        return False
    
    if not check_error():
        return "falha no rally" 


def cmdcount(region):
    if DEBUG_CMD:
        debug(f"[DEBUG] cmdcount chamado com região = {region}")

    encontrados = []

    for i in range(1, 4):
        path = cmd_path(f"cmd{i}.png")

        if DEBUG_CMD:
            debug(f"[DEBUG] tentando localizar: {path}")

        try:
            box = pyautogui.locateOnScreen(path, region=region, confidence=0.7)
        except Exception:
            if DEBUG_CMD:
                debug("[DEBUG] erro locate")
            box = None

        if box:
            encontrados.append(i)

    if DEBUG_CMD:
        debug(f"[DEBUG] contador final = {len(encontrados)}")

    return len(encontrados), encontrados

def verify_and_execute():
    qtd, encontrados = cmdcount(config.REGIONS["CMD"])
    log(f"[CMDCOUNT] qtd={qtd} encontrados={encontrados}")

    if config.active_mode == "mode_1":
        if qtd < 3:
            log("[FLOW] Execution allowed for mode_1 (qtd < 3)")
            return True
        else:
            log("[FLOW] Blocked for mode_1 (qtd >= 3). Sleep 1s")
            time.sleep(1)
            return False

    elif config.active_mode in ("mode_2", "mode_3"):
        if qtd < 1:
            log("[FLOW] Execution allowed for mode_2/mode_3 (qtd < 1)")
            return True
        else:
            log("[FLOW] Blocked for mode_2/mode_3 (qtd >= 1). Sleep 1s")
            time.sleep(1)
            return False

    else:
        log("[FLOW] No valid mode selected")
        return False
    