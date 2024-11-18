import time
import pyautogui


print("Posicione o mouse onde você deseja capturar as coordenadas.")
time.sleep(3)  # Aguarda 5 segundos para você posicionar o mouse

# Captura as coordenadas do mouse
x, y = pyautogui.position()

print(f"As coordenadas do mouse são: ({x}, {y})")