import os
import cv2
import numpy as np

# Função para carregar imagens de um split
def load_split_images(split_folder, target_size=(256, 256)):
    images = []
    labels = []

    # Mapeamento explícito de rótulos
    label_map = {'forgery': 0, 'real': 1, 'motorista': 2}
    
    print(f"Carregando imagens do diretório: {split_folder}")
    
    classes = sorted(os.listdir(split_folder))  # Garantir ordem alfabética consistente

    for label in classes:
        label_normalized = label.lower().strip()  # Normalizar nome da pasta
        if label_normalized not in label_map:
            print(f"Aviso: Pasta '{label}' não reconhecida. Ignorando.")
            continue
        
        # Caminho da pasta da classe
        class_folder = os.path.join(split_folder, label)
        
        # Verificar se a pasta é um diretório
        if not os.path.isdir(class_folder):
            print(f"Aviso: '{class_folder}' não é um diretório. Ignorando.")
            continue

        # Listar arquivos na pasta da classe
        for filename in os.listdir(class_folder):
            if filename.endswith(('.png', '.jpeg', '.jpg')):
                img_path = os.path.join(class_folder, filename)
                print(f"Arquivo encontrado: {filename} (classe: {label})")  # Log para verificar arquivos
                img = cv2.imread(img_path, cv2.IMREAD_COLOR)
                if img is None:
                    print(f"Erro ao carregar a imagem: {img_path}")
                    continue
                img_resized = cv2.resize(img, target_size)
                img_normalized = img_resized / 255.0
                images.append(img_normalized)
                labels.append(label_map[label_normalized])  # Adicionar rótulo como índice

    # Transformar rótulos em one-hot encoding
    labels_one_hot = np.eye(len(label_map))[labels]

    # Debug: Verificar rótulos
    print("Rótulos originais (índices):", labels[:10])
    print("Rótulos one-hot (primeiros 10):", labels_one_hot[:10])
    print(f"Número total de imagens carregadas: {len(images)}")
    
    return np.array(images), labels_one_hot

# Função para salvar embeddings
def save_embeddings(embeddings, labels, file_path):
    np.save(file_path + '/embeddings.npy', embeddings)
    np.savetxt(file_path + '/labels.csv', labels, delimiter=',', fmt='%s')
    print(f"Embeddings salvos em {file_path}/embeddings.npy e {file_path}/labels.csv")