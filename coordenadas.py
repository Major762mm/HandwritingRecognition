import time
import pyautogui
from plyer import notification

def coordenadas():
    print("Posicione o mouse onde você deseja capturar as coordenadas.")
    time.sleep(3)  # Aguarda 3 segundos para você posicionar o mouse

    # Captura as coordenadas do mouse
    x, y = pyautogui.position()

    print(f"As coordenadas do mouse são: ({x}, {y})")
    notificar("Coordenadas coletadas", f"X: {x}, Y: {y}")

def notificar(titulo, mensagem):
    notification.notify(
        title=titulo,
        message=mensagem,
        timeout=2
    )

# Chamando a função para capturar as coordenadas
coordenadas()
