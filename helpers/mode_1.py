from helpers.screen import find_and_click
from helpers.safety import serverc_safety
from helpers.flow import verify_and_execute



def mode_1(stop_event):
    verify_and_execute()

    if stop_event.is_set():
        return

    serverc_safety()

    if stop_event.is_set():
        return

    find_and_click("march.png", region_key="march", confidence=0.30, tries=1)