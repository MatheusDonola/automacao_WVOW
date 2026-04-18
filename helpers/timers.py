import time
import pyautogui
import config

from core.state import STATE
from config import TEMPO_STOP, TEMPO_RESET, SPEED_MODE
from config import COORDS
from helpers.screen import find_image
from helpers.logger import log

def sleep_speed(delay):
    if config.SPEED_MODE == "SLOW":
        time.sleep(delay * 2)
    elif config.SPEED_MODE == "NORMAL":
        time.sleep(delay)
    elif config.SPEED_MODE == "FAST":
        time.sleep(delay * 0.75)
    else:
        time.sleep(delay)

def tempo_estourou_stop():
    return (time.time() - STATE["start"]) >= TEMPO_STOP

def tempo_estourou_reset():
    return (time.time() - STATE["evento_reset"]) >= TEMPO_RESET

def marca_reset_agora():
    STATE["evento_reset"] = time.time()

def executar_reset_geral(timeout = 45):
    log("Executing cache reset")
    x, y = COORDS["RESET"]

    pyautogui.click(x, y)
    time.sleep(1)
    pyautogui.click(x, y)
    time.sleep(1)
    pyautogui.click(x, y)
    sleep_speed(11.5)
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if find_image("world.png", region_key="WORLD", confidence=0.85, pasta="reset"):
            time.sleep(2)
            pyautogui.click(x, y)
            time.sleep(2)
            if not find_image("world.png", region_key="WORLD", confidence=0.85, pasta="reset"):
                marca_reset_agora()
                log("Reset correctly finalized")
                sleep_speed(10)
                return True
    certify_reset()
    return True

def certify_reset():
    if find_image("campaign.png", region_key="campaign", confidence=0.85, pasta="imagens"):
        log("activating fallback")
        time.sleep(2)
        x, y = COORDS["RESET"]
        pyautogui.click(x, y)
        time.sleep(3)
        if not find_image("campaign.png", region_key="campaign", confidence=0.85, pasta="imagens"):
            log("fallback success")
            return True
        else:
            log("recursion activate")
            certify_reset()
