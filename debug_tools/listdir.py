import os

img = r"D:\VSCODE PASTAS\AutomacaoVow\assets\bsfctpath\firelizard.png"

print("img repr:", repr(img))
print("exists:", os.path.exists(img))
print("isfile:", os.path.isfile(img))
print("dir assets:", os.listdir(r"D:\VSCODE PASTAS\AutomacaoVow\assets"))
print("dir bsfctpath:", os.listdir(r"D:\VSCODE PASTAS\AutomacaoVow\assets\bsfctpath"))