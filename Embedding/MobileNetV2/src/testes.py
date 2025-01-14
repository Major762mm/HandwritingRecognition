import os

def rename_images_in_folder(folder_path):
    # Listar todas as imagens no diretório
    for filename in os.listdir(folder_path):
        # Filtrar imagens (supondo que sejam .jpg, .png ou .jpeg)
        if filename.endswith(('.png', '.jpeg', '.jpg')):
            # Obter o nome da classe (a pasta em que a imagem está)
            class_name = os.path.basename(folder_path)
            
            # Criar o novo nome da imagem
            new_name = f"{class_name}_{filename}"
            
            # Caminho completo para a imagem antiga e nova
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            
            # Renomear a imagem
            os.rename(old_path, new_path)
            print(f"Renomeando {filename} para {new_name}")

def rename_images_in_train_split(root_folder):
    # Percorrer todas as subpastas em "train"
    val_folder = os.path.join(root_folder, 'val')
    for class_folder in os.listdir(val_folder):
        class_path = os.path.join(val_folder, class_folder)
        if os.path.isdir(class_path):
            rename_images_in_folder(class_path)

# Caminho para a pasta 'split'
split_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\split'
rename_images_in_train_split(split_folder)
