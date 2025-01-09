import os
import cv2
import numpy as np
from sklearn.preprocessing import LabelBinarizer

# Função para carregar imagens de um split
def load_split_images(split_folder, target_size=(256, 256)):
    images = []
    labels = []
    label_binarizer = LabelBinarizer()

    print(f"Carregando imagens do diretório: {split_folder}")
    
    classes = sorted(os.listdir(split_folder))
    label_binarizer.fit(classes)

    for label in classes:
        class_folder = os.path.join(split_folder, label)
        for filename in os.listdir(class_folder):
            if filename.endswith(('.png', '.jpeg', '.jpg')):
                img_path = os.path.join(class_folder, filename)
                img = cv2.imread(img_path, cv2.IMREAD_COLOR)
                if img is None:
                    print(f"Erro ao carregar a imagem: {img_path}")
                    continue
                img_resized = cv2.resize(img, target_size)
                img_normalized = img_resized / 255.0
                images.append(img_normalized)
                labels.append(label)
    
    print(f"Número total de imagens carregadas: {len(images)}")
    labels_one_hot = label_binarizer.transform(labels)
    return np.array(images), labels_one_hot

# Função para salvar embeddings
def save_embeddings(embeddings, labels, file_path):
    np.save(file_path + '/embeddings.npy', embeddings)
    np.savetxt(file_path + '/labels.csv', labels, delimiter=',', fmt='%s')
    print(f"Embeddings salvos em {file_path}/embeddings.npy e {file_path}/labels.csv")
