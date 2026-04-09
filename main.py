import pyautogui
import time

from core import state

from helpers.flow import verify_and_execute
from helpers.timers import tempo_estourou_stop, tempo_estourou_reset, executar_reset_geral
from helpers.paths import project_dir, assets_dir, img_path, cmd_path
from helpers.safety import serverc_safety
from helpers.flow import find_and_click
from helpers.screen import check_error
from helpers.ocr import read_energy
from helpers import logger
from threading import Event
import config
from core.statistics import STATS
from multiprocessing import Event

logger.DEBUG = config.DEBUG 

def main_loop(stop_event):
    logger.log("=========== INITIALIZING ===========")
    time.sleep(3)
    state.reset_state()
    pyautogui.PAUSE = 0.3
    pyautogui.FAILSAFE = False
    STATS.energia_inicial = read_energy()
    logger.log(f"Starting energy detected: {STATS.energia_inicial}")

    while not stop_event.is_set():
        if tempo_estourou_stop():
            logger.log("Max time reached.")
            break

        if tempo_estourou_reset():
            executar_reset_geral()

        check_error()
        verify_and_execute()
        serverc_safety()
        find_and_click("march.png", region_key="march", confidence=0.30, tries=2)

    if stop_event.is_set():
        logger.log("Stopping requested by user.")
        logger.log("=========== DATA ===========")
        STATS.energia_final = read_energy()
        STATS.close_session()
      

    logger.log("Bot finished.")

if __name__ == "__main__":
    main_loop(Event())