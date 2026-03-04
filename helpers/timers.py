import time
import pyautogui

from core.state import STATE
from config import TEMPO_STOP, TEMPO_RESET
from config import COORDS
from helpers.screen import find_exists

def tempo_estourou_stop():
    return (time.time() - STATE["start"]) >= TEMPO_STOP

def tempo_estourou_reset():
    return (time.time() - STATE["evento_reset"]) >= TEMPO_RESET

def marca_reset_agora():
    STATE["evento_reset"] = time.time()

def executar_reset_geral():
    print("Executando RESET de cache...")

    x, y = COORDS["RESET"]

    pyautogui.click(x, y)
    time.sleep(1)
    pyautogui.click(x, y)
    time.sleep(11)

    pyautogui.click(x, y)
    time.sleep(8)

    if find_exists("error_confirmation.png", region_key="verify",
                start_conf=0.7,
                min_conf=0.3,
                step=0.05,
                retry_delay=0.2,
                pasta="safe"):
        pyautogui.click(x, y)
        time.sleep(8)
        return "error confirmatio corrigido"
    else:
        marca_reset_agora()
        print("RESET finalizado.")