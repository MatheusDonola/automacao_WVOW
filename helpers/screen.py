import time
import os
import pyautogui
import random
from config import REGIONS
from helpers.paths import img_path, cmd_path
from helpers.clicks import click_region

DEBUG = False

def find_exists(nome_img, region_key=None,
                start_conf=0.7,
                min_conf=0.3,
                step=0.05,
                retry_delay=0.2,
                pasta="bsfctpath"):

    path = img_path(nome_img, pasta=pasta)
    region = REGIONS.get(region_key)
    conf = start_conf

    while conf >= min_conf:
        try:
            box = pyautogui.locateOnScreen(path, confidence=conf, region=region)
            if box:
                return True
        except:
            pass

        conf -= step
        time.sleep(retry_delay)

    return False

def find_image(nome_img, region_key=None, confidence=0.45):
    path = img_path(nome_img)
    region = REGIONS.get(region_key)

    try:
        return pyautogui.locateOnScreen(
            path,
            confidence=confidence,
            region=region
        )
    except:
        return None
    

def find_and_click(
    nome_img,
    region_key=None,
    confidence=0.45,
    tries=5,
    retry_delay=0.2,
    jitter=4
):
    for tentativa in range(1, tries + 1):
        box = find_image(nome_img, region_key, confidence)

        if DEBUG:
            print(f"[FIND] {nome_img} try={tentativa}/{tries} "
                  f"region_key={region_key} conf={confidence} box={box}")

        if box:
            x, y = pyautogui.center(box)

            jx = random.randint(-jitter, jitter)
            jy = random.randint(-jitter, jitter)

            x2, y2 = x + jx, y + jy

            if DEBUG:
                print(f"[CLICK] center=({x},{y}) jitter=({jx},{jy}) final=({x2},{y2})")

            pyautogui.click(x2, y2)
            return True

        time.sleep(retry_delay)

    if DEBUG:
        print(f"[FIND] {nome_img} FALHOU após {tries} tentativas")

    return False

def check_rally_initiated(
    img_path,
    *,
    conf,
    region,
    fail_click_xy=None,
    retries=3,
    delay=0.25
):
    for _ in range(retries):
        try:
            rally_box = pyautogui.locateOnScreen(
                img_path("rallyinitiated.png", pasta ="imagens"),
                confidence=conf,
                region=region
            )
        except (pyautogui.ImageNotFoundException, OSError):
            rally_box = None

        if rally_box:
            if fail_click_xy:
                x, y = fail_click_xy
                pyautogui.click(x=x, y=y)
            return False

        time.sleep(delay)

    return True 