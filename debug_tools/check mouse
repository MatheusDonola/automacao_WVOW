import pyautogui
import time

def mouse_pos():
    try:
        while True:
            x, y = pyautogui.position()
            print(f"\rX={x}  Y={y}   ", end="", flush=True)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nParado.")

mouse_pos()