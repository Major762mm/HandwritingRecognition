import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.models import Model
from sklearn.manifold import TSNE
import plotly.express as px
import matplotlib.pyplot as plt

# Diretórios
processed_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\processed'
embedding_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\embeddings'

# Carregar imagens processadas
def load_processed_images(image_folder, target_size=(256, 256)):
    images = []
    labels = []
    print(f"Carregando imagens do diretório: {image_folder}")
    
    for root, dirs, files in os.walk(image_folder):
        for filename in files:
            print(f"Encontrado arquivo: {filename}")  # Print para verificar os arquivos encontrados
            if filename.endswith(".png") or filename.endswith(".jpeg"):
                img_path = os.path.join(root, filename)
                img = cv2.imread(img_path, cv2.IMREAD_COLOR)  # Carregar como imagem colorida
                img_resized = cv2.resize(img, target_size)  # Redimensionar para 256x256
                img_normalized = img_resized / 255.0  # Normaliza a imagem
                images.append(img_normalized)
                label = filename.split("_")[0]  # Extrai rótulo (ajuste conforme o padrão do arquivo)
                labels.append(label)
    
    print(f"Número total de imagens carregadas: {len(images)}")  # Print para verificar o número de imagens
    return np.array(images), np.array(labels)

# Carregar MobileNetV2 para gerar embeddings
def load_mobilenet_embedding_model():
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(256, 256, 3))
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    embedding_model = Model(inputs=base_model.input, outputs=x)
    return embedding_model

# Gerar embeddings
def generate_embeddings(model, images):
    # As imagens já estão na forma correta, não precisamos expandir ou repetir
    embeddings = model.predict(images)  # Passar diretamente as imagens
    return embeddings

# Visualizar embeddings com t-SNE
def visualize_embeddings_tsne(embeddings, labels, interactive=False):
    tsne = TSNE(n_components=2, perplexity=30, max_iter=5000, random_state=42)  # Atualizado para max_iter
    embeddings_2d = tsne.fit_transform(embeddings)
    
    if interactive:
        # Gráfico interativo com Plotly
        fig = px.scatter(
            x=embeddings_2d[:, 0],
            y=embeddings_2d[:, 1],
            color=labels,
            title="t-SNE dos Embeddings (Gráfico Interativo)",
            labels={"x": "Dimensão 1", "y": "Dimensão 2", "color": "Rótulos"}
        )
        fig.show()
    else:
        # Gráfico estático com Matplotlib
        plt.figure(figsize=(10, 8))
        scatter = plt .scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=labels, cmap="tab10")
        plt.colorbar(scatter)
        plt.title("t-SNE dos Embeddings")
        plt.xlabel("Dimensão 1")
        plt.ylabel("Dimensão 2")
        plt.show()

# Salvar embeddings em um arquivo
def save_embeddings(embeddings, labels, file_path):
    np.save(file_path + '/embeddings.npy', embeddings)
    np.savetxt(file_path + '/labels.csv', labels, delimiter=',', fmt='%s')
    print(f"Embeddings salvos em {file_path}/embeddings.npy e {file_path}/labels.csv")

# Função principal
def main():
    images, labels = load_processed_images(processed_folder)
    embedding_model = load_mobilenet_embedding_model()
    embeddings = generate_embeddings(embedding_model, images)
    
    # Salvar os embeddings
    save_embeddings(embeddings, labels, embedding_folder)
    
    # Visualizar os embeddings
    visualize_embeddings_tsne(embeddings, labels, interactive=True)

if __name__ == "__main__":
    main()