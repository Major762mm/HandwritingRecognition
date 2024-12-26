import os

def rename_images_in_folder(folder_path):
    # Verifica se o diretório existe
    if not os.path.exists(folder_path):
        print(f"O diretório {folder_path} não existe.")
        return

    # Lista todos os arquivos no diretório
    files = os.listdir(folder_path)
    count = 1

    for filename in files:
        # Verifica se o arquivo é uma imagem
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            # Cria um novo nome de arquivo
            new_name = f"image_{count}.jpg"  # Você pode mudar a extensão conforme necessário
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_name)

            # Renomeia o arquivo
            os.rename(old_file_path, new_file_path)
            print(f"Renomeado: {old_file_path} -> {new_file_path}")

            count += 1

# Exemplo de uso
if __name__ == "__main__":
    folder_path = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\raw'  # Substitua pelo caminho correto
    rename_images_in_folder(folder_path)