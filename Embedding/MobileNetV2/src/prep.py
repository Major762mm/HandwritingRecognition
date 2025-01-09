import cv2
import numpy as np
import os
import random
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_and_split(input_folder, output_folder, target_size=(256, 256), split_ratios=(0.7, 0.15, 0.15), seed=42):
    """
    Pré-processa as imagens e realiza a divisão em treino, validação e teste.

    Args:
        input_folder (str): Caminho para o diretório de entrada.
        output_folder (str): Caminho para o diretório de saída.
        target_size (tuple): Dimensão alvo para as imagens redimensionadas.
        split_ratios (tuple): Proporções de treino, validação e teste.
        seed (int): Semente para garantir reprodutibilidade.
    """
    random.seed(seed)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Diretório de saída criado: {output_folder}")

    # Pastas para cada categoria
    categories = ["motoristas", "handwritten_signatures/dataset1/real", "handwritten_signatures/dataset1/forge",
                  "handwritten_signatures/dataset2/real", "handwritten_signatures/dataset2/forge",
                  "handwritten_signatures/dataset3/real", "handwritten_signatures/dataset3/forge",
                  "handwritten_signatures/dataset4/real", "handwritten_signatures/dataset4/forge",
                  "handwritten_signatures/dataset5/real", "handwritten_signatures/dataset5/forge"]
    split_folders = ["train", "val", "test"]

    for split in split_folders:
        for category in ["motorista", "real", "forgery"]:
            os.makedirs(os.path.join(output_folder, split, category), exist_ok=True)

    for dataset_type in categories:
        dataset_path = os.path.join(input_folder, dataset_type)
        label_type = "real" if "real" in dataset_type else "forgery" if "forge" in dataset_type else "motorista"

        images = []
        filenames = []
        
        for root, _, files in os.walk(dataset_path):
            for filename in files:
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    img_path = os.path.join(root, filename)
                    
                    # Carregar imagem
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        logging.warning(f"Erro ao carregar a imagem: {img_path}")
                        continue

                    # Suavização inicial para redução de ruído
                    img_blurred = cv2.GaussianBlur(img, (3, 3), 0)

                    # Normalizar (apenas divisão por 255.0)
                    img_normalized = img_blurred / 255.0

                    # Redimensionar com interpolação suave
                    img_resized = cv2.resize(img_normalized, target_size, interpolation=cv2.INTER_LINEAR)

                    # Salvar a imagem processada na memória
                    images.append((img_resized * 255).astype(np.uint8))
                    filenames.append(filename)

        # Realizar divisão em splits
        total_files = len(images)
        indices = list(range(total_files))
        random.shuffle(indices)

        train_end = int(total_files * split_ratios[0])
        val_end = train_end + int(total_files * split_ratios[1])

        splits = {
            "train": indices[:train_end],
            "val": indices[train_end:val_end],
            "test": indices[val_end:]
        }

        # Salvar imagens nos diretórios correspondentes
        for split, split_indices in splits.items():
            for idx in split_indices:
                img = images[idx]
                filename = filenames[idx]
                output_path = os.path.join(output_folder, split, label_type, filename)
                cv2.imwrite(output_path, img)
                logging.info(f"Imagem salva: {output_path}")

    logging.info(f"Pré-processamento e divisão concluídos. Dados salvos em {output_folder}")

# Caminhos de entrada e saída
input_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\raw'
output_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\processed\split'

# Executar pré-processamento e divisão
preprocess_and_split(input_folder, output_folder)
