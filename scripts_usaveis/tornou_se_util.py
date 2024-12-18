import pyautogui
import keyboard

def press_up_arrow():
    # Simula pressionar a tecla seta para cima
    pyautogui.press('right')

# Função para monitorar a tecla "Enter"
def on_enter_press():
    # Quando Enter for pressionado, pressiona a seta para cima
    press_up_arrow()

# Escuta a tecla "Enter"
keyboard.on_press_key("enter", lambda _: on_enter_press())

# Loop infinito para manter o programa em execução
keyboard.wait("esc")  # Use "esc" para fechar o programa
