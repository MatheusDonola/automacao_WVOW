import pyautogui
import time

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)


from helpers.paths import cmd_path
from config import REGIONS

print("DEBUGCMD INICIOU")

def debug_find_cmd14():
    imagem = cmd_path("cmd14.png")
    regiao = REGIONS["CMD"]

    print("\n===== DEBUG CMD14 =====")
    time.sleep(2)
    print(f"Imagem: {imagem}")
    print(f"Região: {regiao}")

    testes = [
        {"confidence": 0.9, "grayscale": False},
        {"confidence": 0.8, "grayscale": False},
        {"confidence": 0.7, "grayscale": False},
        {"confidence": 0.6, "grayscale": False},
        {"confidence": 0.9, "grayscale": True},
        {"confidence": 0.8, "grayscale": True},
        {"confidence": 0.7, "grayscale": True},
        {"confidence": 0.6, "grayscale": True},
    ]

    for teste in testes:
        confidence = teste["confidence"]
        grayscale = teste["grayscale"]

        print(f"\nTestando confidence={confidence} grayscale={grayscale}")

        try:
            pos = pyautogui.locateOnScreen(
                imagem,
                region=regiao,
                confidence=confidence,
                grayscale=grayscale
            )

            if pos:
                centro = pyautogui.center(pos)
                print(f"ACHOU: box={pos} centro={centro}")
            else:
                print("NÃO ACHOU")

        except Exception as e:
            print(f"ERRO: {e}")

        time.sleep(0.3)

if __name__ == "__main__":
    print("ENTRANDO NA FUNÇÃO")
    debug_find_cmd14()