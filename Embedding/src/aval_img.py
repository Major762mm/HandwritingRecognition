import matplotlib.pyplot as plt
import cv2

# Carregar e exibir uma imagem processada
img = cv2.imread('data/processed/motorista_001/motorista_001_img1.jpg', cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray')
plt.title("Imagem Processada")
plt.show()

