from main import main_loop
from helpers import logger
from core.statistics import STATS


def run_bot(stop_event, log_queue):
    logger.log_callback = log_queue.put

    try:
        main_loop(stop_event)

        try:
            log_queue.put("__STATS_START__")
            log_queue.put("=========== STATISTICS ===========")
            log_queue.put(f"Energia inicial: {STATS.energia_inicial}")
            log_queue.put(f"Energia final: {STATS.energia_final}")

            for attr_name, value in vars(STATS).items():
                if attr_name in ("energia_inicial", "energia_final"):
                    continue
                if attr_name.startswith("_"):
                    continue
                log_queue.put(f"{attr_name}: {value}")

            log_queue.put("__STATS_END__")
        except Exception as e:
            try:
                log_queue.put(f"[STATS ERROR] {e}")
            except Exception:
                pass

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