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

logger.DEBUG = False

if __name__ == "__main__":
    print("------ INICIALIZANDO ------")
    time.sleep(3)
    pyautogui.PAUSE = 0.3
    pyautogui.FAILSAFE = False

    while True:
        if tempo_estourou_stop():
            logger.log("Tempo limite atingido.")
            break

        if tempo_estourou_reset():
            executar_reset_geral()

        check_error()
        verify_and_execute()
        serverc_safety()
        find_and_click("march.png", region_key="march", confidence=0.30, tries=2)
