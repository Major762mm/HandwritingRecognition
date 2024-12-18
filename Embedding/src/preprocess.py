import cv2
import os

def preprocess_images(input_dir, output_dir, size=(128, 128)):
    os.makedirs(output_dir, exist_ok=True)
    for folder in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder)
        output_folder = os.path.join(output_dir, folder)
        os.makedirs(output_folder, exist_ok=True)
        
        for file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Escala de cinza
            img = cv2.resize(img, size)  # Padronizar tamanho
            img = cv2.GaussianBlur(img, (5, 5), 0)  # Reduzir ruído
            output_path = os.path.join(output_folder, file)
            cv2.imwrite(output_path, img)

preprocess_images('data/raw', 'data/processed')
