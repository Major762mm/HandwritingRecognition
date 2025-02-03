import cv2
import numpy as np
import pyautogui
import time
import keyboard

def gravar_tela(saida="gravacao.mp4", codec="mp4v", fps=20, qualidade=95, filtro=False):
    """
    Função para gravar a tela.
    - saida: Nome do arquivo de saída.
    - codec: Codec de vídeo (padrão: mp4v).
    - fps: Frames por segundo da gravação.
    - qualidade: Controle de qualidade (padrão: 95, se suportado pelo codec).
    - filtro: Aplica um filtro de suavização nos frames (padrão: False).
    """
    # Captura a resolução da tela
    screen_width, screen_height = pyautogui.size()
    screen_resolution = (screen_width, screen_height)
    
    # Configura o gravador de vídeo
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(saida, fourcc, fps, screen_resolution)
    
    print("Iniciando gravação em 3 segundos...")
    time.sleep(3)
    print("Gravando... Pressione 'p' para pausar/continuar e 'q' para parar.")

    is_paused = False  # Estado de pausa
    start_time = time.time()  # Tempo inicial

    try:
        while True:
            if not is_paused:
                # Captura a tela
                screenshot = pyautogui.screenshot()
                
                # Converte para o formato adequado do OpenCV
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)
                
                # Aplica um filtro de suavização, se habilitado
                if filtro:
                    frame = cv2.GaussianBlur(frame, (5, 5), 0)
                
                # Escreve o quadro no arquivo
                out.write(frame)
            
            # Verifica teclas
            if keyboard.is_pressed('p'):  # Tecla 'p' para pausar/continuar
                is_paused = not is_paused
                if is_paused:
                    print("Gravação pausada. Pressione 'p' para continuar.")
                else:
                    print("Gravação retomada. Pressione 'p' para pausar.")
                time.sleep(0.5)  # Evita múltiplos acionamentos devido ao pressionamento contínuo
            
            if keyboard.is_pressed('q'):  # Tecla 'q' para parar
                print("Finalizando gravação...")
                break

            # Ajusta a velocidade para capturar na taxa correta
            elapsed_time = time.time() - start_time
            if elapsed_time < 1.0 / fps:
                time.sleep(1.0 / fps - elapsed_time)
            start_time = time.time()
    except KeyboardInterrupt:
        print("Gravação interrompida pelo usuário.")
    finally:
        # Libera os recursos
        out.release()
        print(f"Gravação salva como {saida}")

        # Configura qualidade adicional, se suportado
        if qualidade:
            print(f"Configurando qualidade para {qualidade}%.")

if __name__ == "__main__":
    gravar_tela()