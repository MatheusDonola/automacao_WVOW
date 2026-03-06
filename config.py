import os

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
    "CMD_FSTEP":(1739, 225, 62, 407)
}

COORDS = {
    "BACK": (107, 90),
    "RESET": (125, 948),
    "RALLY_FAIL_CLICK": (672, 468),
    "LIZARD_CENTER": (948, 560),
    "FIRELIZARD_CENTER": (614, 943)
}

# ===== TEMPOS =====
TEMPO_STOP = 7240 
TEMPO_RESET = 450  #450 padrão

# ===== COMPORTAMENTO =====
ATAQUE_RAILGUN = True
MAX_TRIES_BACK = 5
DELAY_BACK = 0.6

# ===== CONFIDENCES =====
CONF_DEFAULT = 0.45
CONF_RALLY = 0.30



