import tkinter as tk
import pyautogui
import threading
import time

def atualizar_coordenadas(label):
    """Atualiza as coordenadas do mouse na interface em tempo real."""
    while True:
        # Obtém as coordenadas do mouse
        x, y = pyautogui.position()
        label.config(text=f"X: {x}, Y: {y}")
        time.sleep(0.1)  # Atualiza a cada 100ms

def iniciar_interface():
    """Inicia a interface gráfica para exibir as coordenadas do mouse."""
    # Criação da janela principal
    janela = tk.Tk()
    janela.title("Monitor de Coordenadas do Mouse")
    janela.geometry("300x100")

    # Label para exibir as coordenadas
    label_coordenadas = tk.Label(janela, text="Posicione o mouse para capturar as coordenadas", font=("Arial", 12))
    label_coordenadas.pack(pady=20)

    # Thread para atualizar as coordenadas em tempo real
    thread = threading.Thread(target=atualizar_coordenadas, args=(label_coordenadas,))
    thread.daemon = True  # Define como daemon para encerrar com a aplicação
    thread.start()

    # Inicia o loop da interface
    janela.mainloop()

# Chama a função para iniciar a interface
if __name__ == "__main__":
    iniciar_interface()
