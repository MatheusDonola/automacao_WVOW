import time
import pyautogui

from core.state import STATE
from config import TEMPO_STOP, TEMPO_RESET
from config import COORDS
from helpers.screen import find_exists
from helpers.logger import log

def tempo_estourou_stop():
    return (time.time() - STATE["start"]) >= TEMPO_STOP

def tempo_estourou_reset():
    return (time.time() - STATE["evento_reset"]) >= TEMPO_RESET

def marca_reset_agora():
    STATE["evento_reset"] = time.time()

def executar_reset_geral():
    log("Executando RESET Geral...")
    x, y = COORDS["RESET"]

    pyautogui.click(x, y)
    time.sleep(1)
    pyautogui.click(x, y)
    time.sleep(11)

    pyautogui.click(x, y)
    time.sleep(8)

    marca_reset_agora()
    log("Reset finalizado")