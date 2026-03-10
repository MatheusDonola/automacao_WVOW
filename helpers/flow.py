import pyautogui
import time

from config import REGIONS

from helpers.screen import find_and_click, check_error
from helpers.clicks import click_lizard_center, click_search_center, click_rebel_center
from helpers.paths import img_path
from helpers.screen import find_exists
from helpers.clicks import click_region
from core.statistics import STATS

from helpers.paths import cmd_path
from datetime import datetime

DEBUG_CMD = False
FIRELIZARD = True

def mainfuct():
    if not find_and_click("lupa.png", region_key="lupa", confidence=0.50, tries=5):
        return False

    if FIRELIZARD:
        if not find_and_click("firelizard.png", region_key="firelizard", confidence=0.7, tries=5):
                time.sleep(0.2)
                click_region("firelizard", margin=8, sleep_after=0.2)
                STATS["fallback_firelizard"] +=1
                print(f"Firelizard Fallback ativado ({STATS['fallback_firelizard']})")

    if not find_and_click("search.png", region_key="search", confidence=0.7, tries=5):
        return False
        
    time.sleep(1.6)

    if FIRELIZARD:
        click_lizard_center(delay_before=0.6, jitter=7)
    else:
        click_rebel_center(delay_before=0.5, jitter=8)

    time.sleep(0.2)
  
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

    if not find_and_click("march.png", region_key="march", confidence=0.30, tries=5):
        return False
    
    if not check_error():
        return "falha"


def cmdcount(region):
    if DEBUG_CMD:
        print(f"[DEBUG] cmdcount chamado com região = {region}")

    encontrados = []

    for i in range(1, 4):
        path = cmd_path(f"cmd{i}.png")

        if DEBUG_CMD:
            print(f"[DEBUG] tentando localizar: {path}")

        try:
            box = pyautogui.locateOnScreen(path, region=region, confidence=0.7)
        except Exception:
            if DEBUG_CMD:
                print("[DEBUG] erro locate")
            box = None

        if box:
            encontrados.append(i)

    if DEBUG_CMD:
        print(f"[DEBUG] contador final = {len(encontrados)}")

    return len(encontrados), encontrados

def verify_and_execute():
    qtd, encontrados = cmdcount(REGIONS["CMD"])
    print(f"[CMDCOUNT] qtd={qtd} encontrados={encontrados}")

    if qtd < 3:
        print("[FLOW] Entrando mainfuct() (qtd < 3)")
        result = mainfuct()
        print(f"[FLOW] mainfuct() retornou: {result}")
        return True
    else:
        print("[FLOW] Não vai pro mainfuct (qtd >= 3). Sleep 1s")
        time.sleep(0.2)
        return False