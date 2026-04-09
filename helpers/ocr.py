import re
import pyautogui
import pytesseract
import cv2
import numpy as np
import os
import shutil

from config import REGIONS

tesseract_path = shutil.which("tesseract")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def read_energy(debug=False):
    region = REGIONS["ENERGY"]

    screenshot = pyautogui.screenshot(region=region)

    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.resize(img, None, fx=2, fy=2)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if debug:
        os.makedirs("debug_ocr", exist_ok=True)
        screenshot.save("debug_ocr/energy_raw.png")
        cv2.imwrite("debug_ocr/energy_processed.png", img)

    texto = pytesseract.image_to_string(
        img,
        config='--psm 7 -c tessedit_char_whitelist=0123456789/'
    )

    texto = texto.replace(" ", "").replace("\n", "")
    print("OCR bruto:", texto)

    match = re.search(r"(\d+)/", texto)
    if match:
        return int(match.group(1))

    numeros = re.findall(r"\d+", texto)
    if numeros:
        return int(max(numeros, key=len))

    return None