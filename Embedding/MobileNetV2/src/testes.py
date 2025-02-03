import os

def rename_images_in_folder(folder_path):
    # Obter o nome da classe (a pasta em que a imagem está)
    class_name = os.path.basename(folder_path)
    
    # Inicializar o contador a partir de 1
    counter = 1
    
    # Listar todas as imagens no diretório
    for filename in os.listdir(folder_path):
        # Filtrar imagens (supondo que sejam .jpg, .png ou .jpeg)
        if filename.endswith(('.png', '.jpeg', '.jpg')):
            # Criar o novo nome da imagem com sequência numérica
            new_name = f"{class_name}_{counter}.png"  # Nome desejado
            
            # Caminho completo para a imagem antiga e nova
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            
            # Verificar se o novo nome já existe
            while os.path.exists(new_path):
                counter += 1  # Incrementar o contador
                new_name = f"{class_name}_{counter}.png"  # Criar um novo nome
                new_path = os.path.join(folder_path, new_name)  # Atualizar o caminho
            
            # Renomear a imagem
            os.rename(old_path, new_path)
            print(f"Renomeando {filename} para {new_name}")
            
            # Incrementar o contador
            counter += 1

def rename_images_in_all_splits(root_folder):
    # Definir as pastas de treino, validação e teste
    splits = ['train', 'val', 'test']
    
    # Percorrer cada pasta de split
    for split in splits:
        split_folder = os.path.join(root_folder, split)
        for class_folder in os.listdir(split_folder):
            class_path = os.path.join(split_folder, class_folder)
            if os.path.isdir(class_path):
                rename_images_in_folder(class_path)

# Caminho para a pasta 'split'
split_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\split'
rename_images_in_all_splits(split_folder)