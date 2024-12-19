import cv2
import os
import numpy as np

def preprocess_images(input_dir, output_dir, size=None):  # Tamanho opcional
    os.makedirs(output_dir, exist_ok=True)
    
    for folder in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder)
        
        # Verifica se é um diretório
        if not os.path.isdir(folder_path):
            continue
        
        output_folder = os.path.join(output_dir, folder)
        os.makedirs(output_folder, exist_ok=True)
        
        for file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, file)
            
            # Verifica se é um arquivo de imagem válido
            if not os.path.isfile(img_path):
                continue
            
            try:
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Escala de cinza
                
                if size:  # Redimensiona apenas se necessário
                    img = cv2.resize(img, size)
                
                # Ajustar binarização adaptativa
                img = cv2.adaptiveThreshold(
                    img, 
                    255, 
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY, 
                    15,  # Bloco maior
                    4    # Subtração ajustada
                )

                # Aumentar nitidez
                kernel = np.array([[0, -1, 0],
                                   [-1, 5,-1],
                                   [0, -1, 0]])
                img = cv2.filter2D(img, -1, kernel)

                output_path = os.path.join(output_folder, file)
                cv2.imwrite(output_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            except Exception as e:
                print(f"Erro ao processar {img_path}: {e}")

# Chamada da função
preprocess_images(
    r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\raw',
    r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\processed',
    size=(512, 512)  # Experimente sem ou ajuste o tamanho
)
