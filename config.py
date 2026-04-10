import os

#==== CONFIG ====
DEBUG = False
FIRELIZARD = True
SPEED_MODE = "SLOW"

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
    "WORLD": (20, 871, 191, 202)
}

COORDS = {
    "BACK": (107, 90),
    "RESET": (125, 948),
    "RALLY_FAIL_CLICK": (672, 468),
    "LIZARD_CENTER": (948, 560),
    "FIRELIZARD_CENTER": (614, 943),
    "REBEL":(943,523)
}

# ===== TEMPOS =====
TEMPO_STOP = 6000 #3600 por hora
TEMPO_RESET = 600  #450 padrão ~ 7,5 min

# ===== COMPORTAMENTO =====
ATAQUE_RAILGUN = False
MAX_TRIES_BACK = 5
DELAY_BACK = 0.6

# ===== CONFIDENCES =====
CONF_DEFAULT = 0.45
CONF_RALLY = 0.30

