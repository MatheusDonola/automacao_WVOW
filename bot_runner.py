from main import main_loop
from helpers import logger


def run_bot(stop_event, log_queue):
    logger.log_callback = log_queue.put

    try:
        main_loop(stop_event)
    except Exception as e:
        try:
            log_queue.put(f"[BOT ERROR] {e}")
        except Exception:
            pass
    finally:
        try:
            log_queue.put("__BOT_FINISHED__")
        except Exception:
            pass

        logger.log_callback = None