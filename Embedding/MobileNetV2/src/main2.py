import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2  # type: ignore
from tensorflow.keras.models import Model  # type: ignore
from sklearn.manifold import TSNE
import plotly.express as px
import matplotlib.pyplot as plt

# Pré-processamento das imagens
def preprocess_images(image_folder, target_size=(128, 128)):
    images = []
    labels = []
    for filename in os.listdir(image_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img_path = os.path.join(image_folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img_resized = cv2.resize(img, target_size)
            img_normalized = img_resized / 255.0
            images.append(img_normalized)
            label = filename.split("_")[0]  # Extrai rótulo (ajuste conforme o padrão do arquivo)
            labels.append(label)
    return np.array(images), np.array(labels)

# Carregar MobileNetV2 para gerar embeddings
def load_mobilenet_embedding_model():
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(128, 128, 3))
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    embedding_model = Model(inputs=base_model.input, outputs=x)
    return embedding_model

# Gerar embeddings
def generate_embeddings(model, images):
    images_expanded = np.expand_dims(images, axis=-1)  # Expandir dimensões para grayscale
    images_expanded = np.repeat(images_expanded, 3, axis=-1)  # Converter para 3 canais (RGB)
    embeddings = model.predict(images_expanded)
    return embeddings

# Visualizar embeddings com t-SNE
def visualize_embeddings_tsne(embeddings, labels, interactive=False):
    tsne = TSNE(n_components=2, perplexity=30, n_iter=5000, random_state=42)
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
        scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=labels, cmap="tab10")
        plt.colorbar(scatter)
        plt.title("t-SNE dos Embeddings")
        plt.xlabel("Dimensão 1")
        plt.ylabel("Dimensão 2")
        plt.show()

# Script principal
def main(image_folder, interactive=True):
    print("Pré-processando imagens...")
    images, labels = preprocess_images(image_folder)

    print("Carregando modelo...")
    embedding_model = load_mobilenet_embedding_model()

    print("Gerando embeddings...")
    embeddings = generate_embeddings(embedding_model, images)

    print("Visualizando resultados...")
    visualize_embeddings_tsne(embeddings, labels, interactive=interactive)

# Configurar pasta do dataset e executar
if __name__ == "__main__":
    image_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\processed'  # Substitua pelo caminho correto
    main(image_folder, interactive=True)
