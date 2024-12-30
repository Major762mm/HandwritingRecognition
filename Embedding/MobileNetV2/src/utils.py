import os
import cv2
import numpy as np
from sklearn.preprocessing import LabelBinarizer

# Função para carregar imagens processadas
def load_processed_images(image_folder, target_size=(256, 256)):
    images = []
    labels = []
    print(f"Carregando imagens do diretório: {image_folder}")
    
    for root, dirs, files in os.walk(image_folder):
        for filename in files:
            print(f"Encontrado arquivo: {filename}")
            if filename.endswith(".png") or filename.endswith(".jpeg"):
                img_path = os.path.join(root, filename)
                img = cv2.imread(img_path, cv2.IMREAD_COLOR)
                img_resized = cv2.resize(img, target_size)
                img_normalized = img_resized / 255.0
                images.append(img_normalized)
                label = filename.split("_")[0]  # Extrai rótulo (ajuste conforme o padrão do arquivo)
                labels.append(label)
    
    print(f"Número total de imagens carregadas: {len(images)}")
    return np.array(images), np.array(labels)

# Função para salvar embeddings
def save_embeddings(embeddings, labels, file_path):
    np.save(file_path + '/embeddings.npy', embeddings)
    np.savetxt(file_path + '/labels.csv', labels, delimiter=',', fmt='%s')
    print(f"Embeddings salvos em {file_path}/embeddings.npy e {file_path}/labels.csv")
