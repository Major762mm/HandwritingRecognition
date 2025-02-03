import cv2
import numpy as np
import pyautogui
import time
import os
from datetime import datetime

# Função para garantir que o diretório existe
def criar_diretorio_se_nao_existir(diretorio):
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

# Função para salvar a screenshot
def salvar_screenshot(screenshot, pasta="prints"):
    # Garante que a pasta existe
    criar_diretorio_se_nao_existir(pasta)
    
    # Gera o nome do arquivo com base no horário atual
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho_arquivo = os.path.join(pasta, f"screenshot_{timestamp}.png")
    
    # Salva a imagem
    cv2.imwrite(caminho_arquivo, screenshot)
    print(f"Screenshot salva em: {caminho_arquivo}")

# Função para detectar e clicar na imagem de referência na tela
def detectar_e_clicar_imagem(imagem_referencia, threshold=0.8, pasta="prints"):
    # Captura uma screenshot da tela
    screenshot = pyautogui.screenshot()

    # Converte a screenshot para um formato que o OpenCV entenda (array numpy)
    screenshot = np.array(screenshot)
    
    # Converte para BGR (o OpenCV usa BGR em vez de RGB)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Carrega a imagem de referência
    imagem_template = cv2.imread(imagem_referencia, cv2.IMREAD_COLOR)

    # Usa a correspondência de templates para encontrar a imagem de referência na captura de tela
    resultado = cv2.matchTemplate(screenshot, imagem_template, cv2.TM_CCOEFF_NORMED)
    
    # Encontra as coordenadas do local que melhor corresponde à imagem de referência
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)

    # Se a correspondência for maior que o threshold, consideramos que a imagem foi encontrada
    if max_val >= threshold:
        # Posição onde a imagem foi encontrada
        posicao = max_loc
        
        # Dimensões da imagem de referência
        h, w = imagem_template.shape[:2]
        
        # Desenha um retângulo ao redor da área encontrada (opcional para visualização)
        cv2.rectangle(screenshot, posicao, (posicao[0] + w, posicao[1] + h), (0, 255, 0), 2)
        
        # Salva a screenshot com o retângulo marcado
        salvar_screenshot(screenshot, pasta)
        
        # Move o mouse até a posição detectada e clica
        pyautogui.moveTo(posicao[0] + w//2, posicao[1] + h//2)
        pyautogui.click()
        
        # Retorna a posição central do local encontrado
        return posicao[0] + w//2, posicao[1] + h//2
    else:
        # Salva a screenshot, mesmo quando não encontra a imagem
        salvar_screenshot(screenshot, pasta)
        print("Imagem não encontrada.")
        return None
