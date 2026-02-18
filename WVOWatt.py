import pyautogui
import time
import os
import random   

pyautogui.PAUSE = 0.66
REGIAO_CMD = (1406, 404, 382, 335)
REGIAO_INIT = (560, 300, 780, 70)
REGIAO_START = (1050, 720, 350, 220)
REGIAO_JOGO = (1400, 740, 400, 350)
REGIAO_BACK = (52, 35, 103, 93)


def detectpage():
    base_dir = os.path.dirname(os.path.abspath(__file__)
    back_img = os.path.join(base_dir, "imagens", "radar.png")

    try:
        back = pyautogui.locateOnScreen(
            back_img
            confidence=0.7
            region = REGIAO_BACK
        )
    except pyautogui.ImageNotFoundExcD


def detectgame():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    radar_img = os.path.join(base_dir, "imagens", "radar.png")

    try:
        radar = pyautogui.locateOnScreen(
            radar_img,
            confidence=0.6,
            region=REGIAO_JOGO
        )
    except pyautogui.ImageNotFoundException:
        radar = None
    except ValueError:
        radar = None

    return radar is not None


def detectstart(regiao, confidence=0.7, jitter=10, max_clicks=10):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    march_img = os.path.join(base_dir, "imagens", "march.png")

    clicks = 0
    while clicks < max_clicks:
        try:
            box = pyautogui.locateOnScreen(
                march_img,
                confidence=confidence,
                region=regiao
            )
        except pyautogui.ImageNotFoundException:
            box = None

        if not box:
            return clicks > 0 

        base_x = box.left + box.width // 2
        base_y = box.top + int(box.height * 0.80)

        x = base_x + random.randint(-jitter, jitter)
        y = base_y + random.randint(-jitter, jitter)

        x = max(box.left, min(x, box.left + box.width - 1))
        y = max(box.top,  min(y, box.top + box.height - 1))

        pyautogui.click(x, y)
        clicks += 1
        time.sleep(0.25)

    return True

def basefuct():
    pyautogui.typewrite(["q", "w"], interval=2)
    detectstart(REGIAO_START, confidence=0.7, jitter=10, max_clicks=10)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rally_img = os.path.join(base_dir, "imagens", "rallyinitiated.png")

    try:
        rally = pyautogui.locateOnScreen(
            rally_img,
            confidence=0.8,
            region=REGIAO_INIT
        )
    except pyautogui.ImageNotFoundException:
        rally = None

    if rally:
        pyautogui.click(x=672, y=468)
        print("Falha no init rally (mensagem apareceu)")
        return "falha"
    else:
        print("Sucesso no init rally (mensagem NÃO apareceu)")
        return "sucesso"

def cmdcount(regiao):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_cmds = os.path.join(base_dir, "cmds")
    arquivos = ["cmd1.png", "cmd2.png", "cmd3.png"]
    caminhos = [os.path.join(pasta_cmds, nome) for nome in arquivos]

    for p in caminhos:
        if not os.path.exists(p):
            raise FileNotFoundError(f"Não achei comandantes disponíveis: {p}")

    contador = 0
    encontrados = []
    for caminho in caminhos:
        try:
            achou = pyautogui.locateOnScreen(
                caminho,
                confidence=0.8,
                region=regiao
            )
        except Exception as e:
            print(f"Erro lendo/achando {caminho}: {e}")
            achou = None

        if achou:
            contador += 1
            encontrados.append(os.path.basename(caminho))

    return contador, encontrados

print("Inicializando")

time.sleep(3)

while True:
    print("detectgame:", detectgame())

    if detectgame():
        qtd, quais = cmdcount(REGIAO_CMD)
        print("CMD detectados:", qtd, quais)

        if qtd < 3:
            basefuct()

        time.sleep(1)
    else:
        time.sleep(3)
