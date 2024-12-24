import cv2
import numpy as np
import os

def preprocess_images(image_folder, target_size=(128, 128)):
    images = []
    labels = []
    for filename in os.listdir(image_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # Carregar imagem
            img_path = os.path.join(image_folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            
            # Redimensionar
            img_resized = cv2.resize(img, target_size)
            
            # Normalizar
            img_normalized = img_resized / 255.0
            
            images.append(img_normalized)
            
            # Extrair rótulo do nome do arquivo (opcional)
            label = filename.split("_")[0]  # Exemplo: "pessoa1_img1.png"
            labels.append(label)
    
    return np.array(images), np.array(labels)
