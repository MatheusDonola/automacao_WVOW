import pyautogui
import time

from core.state import STATE

from helpers.flow import verify_and_execute
from helpers.timers import tempo_estourou_stop, tempo_estourou_reset, executar_reset_geral
from helpers.paths import project_dir, assets_dir, img_path, cmd_path
from helpers.safety import serverc_safety
from helpers.flow import find_and_click
from helpers.screen import check_error
from helpers import logger
from threading import Event
import config
from core.statistics import STATS

logger.DEBUG = config.DEBUG

stop_event = Event()

def request_stop():
    stop_event.set()

def clear_stop():
    stop_event.clear()

def main_loop():
    clear_stop()

    logger.log("------ INICIALIZANDO ------")
    time.sleep(3)
    pyautogui.PAUSE = 0.3
    pyautogui.FAILSAFE = False

    while not stop_event.is_set():
        if tempo_estourou_stop():
            logger.log("Tempo limite atingido.")
            break

        if tempo_estourou_reset():
            executar_reset_geral()

        check_error()
        verify_and_execute()
        serverc_safety()
        find_and_click("march.png", region_key="march", confidence=0.30, tries=2)

    if stop_event.is_set():
        logger.log("Parada solicitada pelo usuário.")
        logger.log("======== DATA ========")
        print("STATS type:", type(STATS))
        print("TEM close_session?", hasattr(STATS, "close_session"))
        STATS.close_session()
      

    logger.log("Bot finalizado.")

if __name__ == "__main__":
    main_loop()