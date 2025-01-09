import os
import cv2
import numpy as np
import random
import logging
from albumentations import (HorizontalFlip, VerticalFlip, Rotate, RandomBrightnessContrast,
                            GaussianBlur, ShiftScaleRotate, RandomSizedCrop, CLAHE, Compose)

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def augment_image(image, augmentations):
    """
    Aplica transformações de data augmentation a uma imagem.

    Args:
        image (numpy.ndarray): Imagem de entrada.
        augmentations (albumentations.Compose): Lista de transformações.

    Returns:
        numpy.ndarray: Imagem transformada.
    """
    augmented = augmentations(image=image)
    return augmented["image"]

def augment_dataset(input_folder, output_folder, augmentations, augment_count=5):
    """
    Aumenta o dataset aplicando transformações em imagens existentes.

    Args:
        input_folder (str): Caminho para o diretório de entrada com imagens originais.
        output_folder (str): Caminho para o diretório de saída onde as imagens aumentadas serão salvas.
        augmentations (albumentations.Compose): Lista de transformações a serem aplicadas.
        augment_count (int): Número de novas imagens a gerar para cada imagem original.

    Returns:
        None
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Diretório de saída criado: {output_folder}")

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(root, file)
                image = cv2.imread(img_path)
                if image is None:
                    logging.warning(f"Erro ao carregar imagem: {img_path}")
                    continue

                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_subfolder):
                    os.makedirs(output_subfolder)

                base_name, ext = os.path.splitext(file)
                for i in range(augment_count):
                    augmented_image = augment_image(image, augmentations)
                    output_filename = f"{base_name}_aug_{i+1}{ext}"
                    output_path = os.path.join(output_subfolder, output_filename)
                    cv2.imwrite(output_path, augmented_image)
                    logging.info(f"Imagem aumentada salva em: {output_path}")

if __name__ == "__main__":
    # Caminhos
    input_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\processed'
    output_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\augmentation'

    # Definir transformações
    augmentations = Compose([
        HorizontalFlip(p=0.5),
        VerticalFlip(p=0.5),
        Rotate(limit=30, p=0.7),
        RandomBrightnessContrast(p=0.6),
        GaussianBlur(p=0.3),
        ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15, p=0.8),
        CLAHE(p=0.4),
        RandomSizedCrop(min_max_height=(200, 256), height=256, width=256, p=0.5)
    ])

    # Executar aumento de dados
    augment_dataset(input_folder, output_folder, augmentations, augment_count=10)
    logging.info("Aumento do dataset concluído.")
