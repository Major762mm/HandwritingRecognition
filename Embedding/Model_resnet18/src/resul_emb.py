import matplotlib.pyplot as plt
import cv2


# Exemplo de visualização
img = cv2.imread(r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\processed\Paulo Cesar S. - Fiorino 50\WhatsApp Image 2024-12-23 at 17.30.09.jpeg', cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray')
plt.title("Imagem Processada")
plt.show()
