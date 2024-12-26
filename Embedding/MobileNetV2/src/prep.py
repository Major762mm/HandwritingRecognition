import cv2
import numpy as np
import os
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_images(input_folder, output_folder, target_size=(128, 128)):
    """
    Pré-processa imagens de um diretório e salva no diretório de saída, percorrendo subpastas.

    Args:
        input_folder (str): Caminho para o diretório de entrada.
        output_folder (str): Caminho para o diretório de saída.
        target_size (tuple): Dimensão alvo para as imagens redimensionadas.

    Returns:
        tuple: Arrays numpy contendo imagens e rótulos.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Diretório de saída criado: {output_folder}")

    images = []
    labels = []

    # Percorrer diretórios e subdiretórios
    for root, dirs, files in os.walk(input_folder):
        logging.info(f"Explorando diretório: {root}")
        for filename in files:
            # Verificar extensão do arquivo (insensível a maiúsculas/minúsculas)
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                img_path = os.path.join(root, filename)
                logging.info(f"Processando arquivo: {img_path}")

                # Carregar imagem
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    logging.warning(f"Erro ao carregar a imagem (possivelmente corrompida ou formato não suportado): {img_path}")
                    continue
                
                # Redimensionar
                img_resized = cv2.resize(img, target_size)
                
                # Normalizar
                img_normalized = img_resized / 255.0
                images.append(img_normalized)
                
                # Salvar imagem pré-processada
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_subfolder):
                    os.makedirs(output_subfolder)
                processed_path = os.path.join(output_subfolder, filename)
                cv2.imwrite(processed_path, (img_normalized * 255).astype(np.uint8))
                logging.info(f"Imagem salva em: {processed_path}")
                
                # Extrair rótulo do nome do arquivo
                label = filename.split("_")[0]  # Exemplo: "pessoa1_img1.png"
                labels.append(label)
            else:
                logging.info(f"Arquivo ignorado devido à extensão: {filename}")

    return np.array(images), np.array(labels)

# Caminhos de entrada e saída
input_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\raw'
output_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\processed'

# Executar pré-processamento
images, labels = preprocess_images(input_folder, output_folder)
logging.info(f"{len(images)} imagens pré-processadas salvas em: {output_folder}")
logging.info(f"Rótulos extraídos: {labels}")
