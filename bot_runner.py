from main import main_loop
from helpers import logger


def run_bot(stop_event, log_queue):
    logger.log_callback = log_queue.put

    try:
        main_loop(stop_event)
    finally:
        try:
            log_queue.put("__BOT_FINISHED__")
        except Exception:
            pass

        logger.log_callback = None