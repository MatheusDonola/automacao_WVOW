import time
import pyautogui

from core.state import STATE
from config import TEMPO_STOP, TEMPO_RESET
from config import COORDS

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
    time.sleep(11)

    pyautogui.click(x, y)
    time.sleep(11)

    marca_reset_agora()
    print("RESET finalizado.")