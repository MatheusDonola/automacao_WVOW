import pyautogui
import time
import os

from config import REGIONS, COORDS

from helpers.screen import find_and_click, check_rally_initiated
from helpers.clicks import click_lizard_center, click_search_center
from helpers.paths import img_path
from helpers.screen import find_exists
from helpers.clicks import click_region

from helpers.paths import cmd_path
from datetime import datetime

DEBUG_CMD = False

def mainfuct():
    if not find_and_click("lupa.png", region_key="lupa", confidence=0.50, tries=5):
        if find_exists("diamond.png", region_key="safe_diamond", start_conf=0.80, min_conf=0.50, pasta="safe"):
            click_region("lupa", margin=8, sleep_after=0.2)
        else:
            return False
    if not find_and_click("firelizard.png", region_key="firelizard", confidence=0.7, tries=5):
            time.sleep(0.2)
            click_region("firelizard", margin=8, sleep_after=0.2)

    click_search_center(delay_before=0.6, jitter=6)

    time.sleep(1.4)

    click_lizard_center(delay_before=0.6, jitter=7)

    time.sleep(1)
  
    if not find_and_click(
        "rally.png",
        region_key="rally",
        confidence=0.45,
        tries=12,           #tries x delay ~1.4seg tot= 2.4
        retry_delay=0.15
    ):
        return False

    if not find_and_click("march.png", region_key="march", confidence=0.30, tries=5):
        return False
    
    ok = check_rally_initiated(
    img_path,
    conf=0.7,
    region=REGIONS["INIT"],
    fail_click_xy=COORDS["RALLY_FAIL_CLICK"],
    retries=3,
    delay=0.25
)
    return "sucesso" if ok else "falha"

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