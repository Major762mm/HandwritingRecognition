# preprocess_simple.py
import cv2
import os
import numpy as np

def preprocess_images(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    for folder in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder)
        
        if not os.path.isdir(folder_path):
            continue
        
        output_folder = os.path.join(output_dir, folder)
        os.makedirs(output_folder, exist_ok=True)
        
        for file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, file)
            
            if not os.path.isfile(img_path):
                continue
            
            try:
                # Carregar imagem em escala de cinza
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                
                # Aplicar binarização (preto e branco)
                _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                # Realce de nitidez (opcional para melhorar as letras)
                kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])  # Kernel de nitidez
                img = cv2.filter2D(img, -1, kernel)
                
                # Salvar imagem processada
                output_path = os.path.join(output_folder, file)
                cv2.imwrite(output_path, img)
            except Exception as e:
                print(f"Erro ao processar {img_path}: {e}")

# Chamada da função
preprocess_images(
    r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\Model_resnet18\data\raw',
    r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\Model_resnet18\data\processed'
)
