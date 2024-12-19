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
                
                # Suavização com filtro bilateral (reduzido)
                img = cv2.bilateralFilter(img, 5, 50, 50)  # Suavização mais leve
                
                # Contraste adaptativo com CLAHE
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                img = clahe.apply(img)
                
                # Realce de nitidez
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
    r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\raw',
    r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\processed'
)
