import cv2
import numpy as np
import pyautogui

# Lista para armazenar as coordenadas das caixas
caixas = []

# Função de callback para capturar as coordenadas do mouse
def draw_rectangle(event, x, y, flags, param):
    global x1, y1, drawing, img, img_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x1, y1 = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (x1, y1), (x, y), (0, 255, 0), 2)
            cv2.imshow('Captura e Marcação', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x2, y2 = x, y
        caixas.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'classe': 'objeto'})
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Configurações da captura de tela
screen_region = (0, 0, 1920, 1080)  # Ajuste a região da tela conforme necessário

# Captura a tela
img = pyautogui.screenshot(region=screen_region)
img = np.array(img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
img_copy = img.copy()

drawing = False

# Exibir a imagem e configurar a função de callback
cv2.namedWindow('Captura e Marcação')
cv2.setMouseCallback('Captura e Marcação', draw_rectangle)

while True:
    cv2.imshow('Captura e Marcação', img)
    if cv2.waitKey(1) & 0xFF == 27:  # Pressionar Esc para sair
        break

cv2.destroyAllWindows()

# Agora a lista "caixas" contém as coordenadas de todas as caixas desenhadas
print(caixas)
