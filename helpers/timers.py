import time
import pyautogui

from core.state import STATE
from config import TEMPO_STOP, TEMPO_RESET
from config import COORDS
from helpers.screen import find_exists, find_image
from helpers.logger import log

def tempo_estourou_stop():
    return (time.time() - STATE["start"]) >= TEMPO_STOP

def tempo_estourou_reset():
    return (time.time() - STATE["evento_reset"]) >= TEMPO_RESET

def marca_reset_agora():
    STATE["evento_reset"] = time.time()

def executar_reset_geral(timeout = 25):
    log("Executing cache reset")
    x, y = COORDS["RESET"]

    pyautogui.click(x, y)
    time.sleep(1)
    pyautogui.click(x, y)
    time.sleep(11)
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if find_image("world.png", region_key="WORLD", confidence=0.85, pasta="reset"):
            time.sleep(2)
            pyautogui.click(x, y)
            time.sleep(2)
            if not find_image("world.png", region_key="WORLD", confidence=0.85, pasta="reset"):
                marca_reset_agora()
                log("Reset correctly finalized")
                time.sleep(5)
                return True

    pyautogui.click(x, y)
    time.sleep(5)
    marca_reset_agora()
    log("Reset finalized by fallback")
    return False