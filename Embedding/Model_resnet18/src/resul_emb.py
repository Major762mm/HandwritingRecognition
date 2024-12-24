import matplotlib.pyplot as plt
import cv2


# Exemplo de visualização
img = cv2.imread(r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\processed', cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray')
plt.title("Imagem Processada")
plt.show()
