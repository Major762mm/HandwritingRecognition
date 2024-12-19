import cv2
import os

def preprocess_images(input_dir, output_dir, size=(256, 256)):
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
                img = cv2.resize(img, size)  # Padronizar tamanho
                #img = cv2.GaussianBlur(img, (5, 5), 0)  # Reduzir ruído
                # Exemplo de binarização adaptativa:
                img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

                output_path = os.path.join(output_folder, file)
                cv2.imwrite(output_path, img)
            except Exception as e:
                print(f"Erro ao processar {img_path}: {e}")

# Chamada da função
preprocess_images(
    r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\raw',
    r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\processed'
)
