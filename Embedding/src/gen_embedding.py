# gen_embedding.py
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import os
import numpy as np

# Modelo pré-treinado
model = models.resnet18(pretrained=True)
model.fc = torch.nn.Identity()  # Remove a camada de classificação

# Transformações para entrada
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])  # Normalização ajustada para [0, 1] e std
])

def generate_embeddings(image_dir, model, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    model.eval()
    
    with torch.no_grad():
        for folder in os.listdir(image_dir):
            folder_path = os.path.join(image_dir, folder)
            
            # Verifica se é um diretório
            if not os.path.isdir(folder_path):
                continue
            
            embeddings = []
            for file in os.listdir(folder_path):
                img_path = os.path.join(folder_path, file)
                
                # Verifica se é um arquivo de imagem válido
                if not os.path.isfile(img_path) or not img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                
                try:
                    img = Image.open(img_path).convert('RGB')  # Converte para RGB
                    img = transform(img).unsqueeze(0)
                    embedding = model(img).numpy()
                    embeddings.append(embedding.flatten())
                except Exception as e:
                    print(f"Erro ao processar {img_path}: {e}")
            
            # Salvar embeddings como NumPy
            if embeddings:
                output_path = os.path.join(output_dir, f"{folder}.npy")
                np.save(output_path, np.array(embeddings))
                print(f"Embeddings salvos em: {output_path}")

    # Exemplo de carregamento e verificação de embeddings
    test_embedding_path = os.path.join(output_dir, 'motorista_001.npy')
    if os.path.exists(test_embedding_path):
        embedding = np.load(test_embedding_path)
        print(f"Forma dos embeddings: {embedding.shape}")
        print("Primeiro embedding:", embedding[0])
    else:
        print(f"Arquivo de embeddings não encontrado: {test_embedding_path}")

# Chamada da função
generate_embeddings(r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\processed', model, r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\embeddings')
