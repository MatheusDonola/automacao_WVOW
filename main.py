import pyautogui
import time

from core import state

from helpers.flow import verify_and_execute
from helpers.timers import tempo_estourou_stop, tempo_estourou_reset, executar_reset_geral
from helpers.safety import serverc_safety
from helpers.flow import find_and_click, cmdcount
from helpers.screen import check_error
from helpers.ocr import read_energy
from helpers import logger
import config
from core.statistics import STATS

logger.DEBUG = config.DEBUG

def main_loop():
    logger.log("------ INICIALIZANDO ------")
    time.sleep(3)
    state.reset_state()
    pyautogui.PAUSE = 0.3
    pyautogui.FAILSAFE = False

    STATS.energia_inicial = read_energy()
    logger.log(f"Energia inicial detectada: {STATS.energia_inicial}")

    try:
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

    except KeyboardInterrupt:
        print("Parada solicitada pelo usuário.")

    finally:
        try:
            print("======== DATA ========")

            qtd_em_andamento, encontrados = cmdcount(config.REGIONS["CMD"])
            STATS.rallies_em_andamento = qtd_em_andamento
            print(f"Rallies em andamento detectados: {qtd_em_andamento} -> {encontrados}")

            STATS.energia_final = read_energy()
            print(f"Energia final detectada: {STATS.energia_final}")

            STATS.close_session()
            print("Bot finalizado.")
        except KeyboardInterrupt:
            print("Finalização interrompida.")
        except Exception as e:
            print(f"Erro ao fechar sessão: {e}")


if __name__ == "__main__":
    main_loop()