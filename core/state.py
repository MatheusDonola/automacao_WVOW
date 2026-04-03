import time

STATE = {
    "start": time.time(),
    "evento_reset": time.time(),
}

def reset_state():
    agora = time.time()
    STATE["start"] = agora
    STATE["evento_reset"] = agora

def tempo_total():
    return time.time() - STATE["start"]

def tempo_desde_reset():
    return time.time() - STATE["evento_reset"]