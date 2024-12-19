import matplotlib.pyplot as plt
import cv2


# Exemplo de visualização
img = cv2.imread('data/processed/exemplo.png', cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray')
plt.title("Imagem Processada")
plt.show()
