import os
import cv2
import numpy as np

def load_images_from_folder(input_folder, target_size=(128, 128)):
    images = []
    labels = []
    # Verificar se o diretório existe
    if not os.path.exists(input_folder):
        print(f"O diretório {input_folder} não existe.")
        return np.array(images), labels

    # Listar os arquivos no diretório e subpastas
    print(f"Arquivos encontrados no diretório {input_folder}:")
    
    for root, dirs, files in os.walk(input_folder):  # Use walk para percorrer subpastas
        for filename in files:
            print(f" - {filename}")
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                img_path = os.path.join(root, filename)
                img = cv2.imread(img_path, cv2.IMREAD_COLOR)  # Leitura das imagens em RGB
                if img is None:
                    print(f"Erro ao carregar a imagem: {img_path}")
                    continue
                
                # Redimensionar imagem para o tamanho de entrada do modelo
                img_resized = cv2.resize(img, target_size)
                
                # Normalizar imagem
                img_normalized = img_resized / 255.0
                images.append(img_normalized)

                # Salvar o nome do arquivo como label
                labels.append(filename)

    return np.array(images), labels

# Caminho da pasta com as imagens
input_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data'

# Carregar imagens do diretório
images, labels = load_images_from_folder(input_folder)

if images.shape[0] > 0:
    print(f"Imagens carregadas: {images.shape[0]}")
else:
    print("Nenhuma imagem válida foi encontrada no diretório.")
