import os
import re
from pathlib import Path

#==== CONFIG ====
DEBUG = False
FIRELIZARD = True
SPEED_MODE = "NORMAL"
active_mode = "mode_2"
DRAG_START = None

#====REGIONS=====
REGIONS = {
    "CMD": (1406, 404, 382, 335),
    "lupa": (1689, 888, 157, 146),
    "firelizard": (535, 878, 145, 131),
    "search": (272, 708, 456, 87),
    "lizard": (805, 409, 436, 367),
    "rally": (1292, 707, 222, 40),
    "march": (964, 684, 456, 269),
    "INIT": (560, 300, 780, 70),
    "safe_diamond": (1579, 33, 86, 65),
    "serverc":(116, 30, 120, 106),
    "verify":(204, 253, 109, 128),
    "CMD_FSTEP":(1739, 225, 62, 407),
    "attk":(1242, 664, 131, 47),
    "ENERGY":(94, 201, 200, 44),
    "lupa_click":(1773, 977, 56, 40),
    "WORLD": (20, 871, 191, 202),
    "RESET": (757, 619, 375, 105),
    "events": (1361, 113, 464, 268),
    "tower": (48, 142, 294, 883),
    "summoner": (1291, 928, 393, 100),
    "error": (1720, 36, 110, 78),
    "campaign": (1648, 864, 214, 178),
    "display": (657, 114, 565, 787),
    "railgun": (60, 156, 112, 882),
    "SUM_RAIL": (1438, 865, 343, 92)
}

COORDS = {
    "BACK": (107, 90),
    "RESET": (125, 948),
    "RALLY_FAIL_CLICK": (672, 468),
    "LIZARD_CENTER": (948, 560),
    "FIRELIZARD_CENTER": (614, 943),
    "REBEL":(943,523)
}

MODE_2_DRAG = {
    "end_x": 718,
    "end_y": 395,
    "duration": 0.5
}

# ===== TEMPOS =====
TEMPO_STOP = 10000 #3600 por hora
TEMPO_RESET = 600  #450 padrão ~ 7,5 min

# ===== COMPORTAMENTO =====
ATAQUE_RAILGUN = False
MAX_TRIES_BACK = 5
DELAY_BACK = 0.6

# ===== CONFIDENCES =====
CONF_DEFAULT = 0.45
CONF_RALLY = 0.30

def update_config_value(key: str, value: str) -> None:
    config_path = Path(__file__).resolve()

    content = config_path.read_text(encoding="utf-8")

    pattern = rf"^{key}\s*=.*$"
    replacement = f"{key} = {value}"

    new_content, count = re.subn(
        pattern,
        replacement,
        content,
        flags=re.MULTILINE
    )

    if count == 0:
        raise ValueError(f"Chave '{key}' não encontrada no config.py")

    config_path.write_text(new_content, encoding="utf-8")