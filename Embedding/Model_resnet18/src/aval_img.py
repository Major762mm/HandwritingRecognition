import matplotlib.pyplot as plt
import cv2

# Carregar e exibir uma imagem processada
img = cv2.imread(r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\processed\Paulo Cesar S. - Fiorino 50\WhatsApp Image 2024-12-23 at 17.30.09', cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray')
plt.title("Imagem Processada")
plt.show()

