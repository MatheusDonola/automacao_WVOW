import pyautogui
import time
from multiprocessing import Event

from core import state
from helpers.flow import verify_and_execute
from helpers.timers import tempo_estourou_stop, tempo_estourou_reset, executar_reset_geral
from helpers.safety import serverc_safety, connection_reset
from helpers.flow import find_and_click
from helpers.screen import check_error
from helpers.ocr import read_energy
from helpers import logger
from core.statistics import STATS
from helpers.mode_1 import mode_1
from helpers.mode_2 import mode_2
from helpers.mode_3 import mode_3
import config

logger.DEBUG = config.DEBUG
active_mode = config.active_mode

def main_loop(stop_event):
    logger.log("=========== INITIALIZING ===========")
    time.sleep(3)
    state.reset_state()
    pyautogui.PAUSE = 0.3
    pyautogui.FAILSAFE = False

    STATS.energia_inicial = read_energy()
    logger.log(f"Starting energy detected: {STATS.energia_inicial}")

    try:
        while not stop_event.is_set():
            if tempo_estourou_stop():
                logger.log("Max time reached.")
                break

            if tempo_estourou_reset():
                executar_reset_geral()

            check_error()
            connection_reset(stop_event)

            if stop_event.is_set():
                break

            if active_mode == "mode_1":
                mode_1(stop_event)
            elif active_mode == "mode_2":
                mode_2(stop_event)
            elif active_mode == "mode_3":
                mode_3(stop_event)
            else:
                logger.log(f"[MODE ERROR] Modo inválido: {active_mode}")
                break

    finally:
        if stop_event.is_set():
            logger.log("Stopping requested by user.")

        logger.log("=========== DATA ===========")

        try:
            STATS.energia_final = read_energy()
        except Exception as e:
            logger.log(f"[FINALIZE ERROR] read_energy falhou: {e}")
            STATS.energia_final = None

        try:
            STATS.close_session()
        except Exception as e:
            logger.log(f"[FINALIZE ERROR] close_session falhou: {e}")

        logger.log("Bot finished.")


if __name__ == "__main__":
    main_loop(Event())