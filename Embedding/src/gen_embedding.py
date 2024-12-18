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
    transforms.Normalize([0.5], [0.5])  # Normalização
])

def generate_embeddings(image_dir, model, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    model.eval()
    
    with torch.no_grad():
        for folder in os.listdir(image_dir):
            folder_path = os.path.join(image_dir, folder)
            embeddings = []
            for file in os.listdir(folder_path):
                img_path = os.path.join(folder_path, file)
                img = Image.open(img_path)
                img = transform(img).unsqueeze(0)
                embedding = model(img).numpy()
                embeddings.append(embedding.flatten())
            
            # Salvar embeddings como NumPy
            output_path = os.path.join(output_dir, f"{folder}.npy")
            np.save(output_path, np.array(embeddings))

        embedding = np.load('data/embeddings/motorista_001.npy')
        print(f"Forma dos embeddings: {embedding.shape}")
        print("Primeiro embedding:", embedding[0])
generate_embeddings('data/processed', model, 'data/embeddings')
