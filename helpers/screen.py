import time
import os
import pyautogui
import random
from config import REGIONS, COORDS
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

def check_error(
    icon_names=("footstep.png", "heal.png"),
    region=REGIONS["CMD_FSTEP"],
    back_click_xy=COORDS["LIZARD_CENTER"],
    timeout=0.9,
    start_conf=0.80,
    min_conf=0.55,
    step=0.05,
    poll_delay=0.05,
    click_delay=0.20
):
    if isinstance(icon_names, str):
        icon_names = (icon_names,)

    paths = [img_path(icon_name, pasta="imagens") for icon_name in icon_names]
    end = time.time() + timeout

    time.sleep(0.05)

    while time.time() < end:
        conf = start_conf
        while conf >= min_conf:
            for path in paths:
                try:
                    box = pyautogui.locateOnScreen(
                        path,
                        confidence=conf,
                        region=region,
                        grayscale=True
                    )
                    if box:
                        if back_click_xy:
                            pyautogui.click(back_click_xy)
                            time.sleep(click_delay)
                        return False
                except:
                    pass
            conf -= step

        time.sleep(poll_delay)

    return True