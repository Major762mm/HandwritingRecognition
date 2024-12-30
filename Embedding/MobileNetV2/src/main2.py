import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2 # type: ignore
from tensorflow.keras.models import Model # type: ignore
from sklearn.manifold import TSNE
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelBinarizer

os.environ["TF_USE_LEGACY_KERAS"] = "1"

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

# Ajuste fino da MobileNetV2
def fine_tune_mobilenet(model, images, labels, epochs=5):
    # Transformar rótulos em one-hot encoding
    lb = LabelBinarizer()
    labels_one_hot = lb.fit_transform(labels)
    
    # Compilação e treinamento do modelo
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Treinar o modelo e capturar o histórico
    history = model.fit(images, labels_one_hot, epochs=epochs, batch_size=16)
    
    return model, history

# Carregar MobileNetV2 para gerar embeddings
def load_mobilenet_embedding_model(num_classes):
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(256, 256, 3))
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(512, activation='relu')(x)  # Opcional: adicionar uma camada intermediária
    output = tf.keras.layers.Dense(num_classes, activation='softmax')(x)  # Saída para classificação
    embedding_model = Model(inputs=base_model.input, outputs=output)
    return embedding_model


# Gerar embeddings
def generate_embeddings(model, images):
    embeddings = model.predict(images)  # Passar diretamente as imagens
    return embeddings

# Visualizar embeddings com t-SNE
def visualize_embeddings_tsne(embeddings, labels, save_as_html=False):
    tsne = TSNE(n_components=2, perplexity=30, n_iter=5000, random_state=42)  # Atualizado para n_iter
    embeddings_2d = tsne.fit_transform(embeddings)

    # Gráfico interativo com Plotly
    fig = px.scatter(
        x=embeddings_2d[:, 0],
        y=embeddings_2d[:, 1],
        color=labels,
        title="t-SNE dos Embeddings (Gráfico Interativo)",
        labels={"x": "Dimensão 1", "y": "Dimensão 2", "color": "Rótulos"}
    )
    
    if save_as_html:
        output_path = os.path.join(embedding_folder, "resultado_tsne.html")
        fig.write_html(output_path)
        print(f"Gráfico interativo salvo como '{output_path}'. Abra-o no navegador.")
    else:
        fig.show()

# Salvar embeddings em um arquivo
def save_embeddings(embeddings, labels, file_path):
    np.save(file_path + '/embeddings.npy', embeddings)
    np.savetxt(file_path + '/labels.csv', labels, delimiter=',', fmt='%s')
    print(f"Embeddings salvos em {file_path}/embeddings.npy e {file_path}/labels.csv")

# Função para plotar gráficos de treinamento
def plot_training_history(history):
    # Plotando a perda e a precisão
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    # Gráfico de perda
    axs[0].plot(history.history['loss'], label='Perda')
    axs[0].set_title('Perda ao Longo das Épocas')
    axs[0].set_xlabel('Épocas')
    axs[0].set_ylabel('Perda')
    axs[0].legend()

    # Gráfico de precisão
    axs[1].plot(history.history['accuracy'], label='Precisão')
    axs[1].set_title('Precisão ao Longo das Épocas')
    axs[1].set_xlabel('Épocas')
    axs[1].set_ylabel('Precisão')
    axs[1].legend()

    plt.tight_layout()
    plt.show()

# Função principal
def main():
    images, labels = load_processed_images(processed_folder)
    num_classes = len(set(labels))  # Determina o número de classes únicas nos rótulos
    embedding_model = load_mobilenet_embedding_model(num_classes)
    embedding_model, history = fine_tune_mobilenet(embedding_model, images, labels, epochs=10)
    embeddings = generate_embeddings(embedding_model, images)
    
    # Salvar os embeddings
    save_embeddings(embeddings, labels, embedding_folder)
    
    # Visualizar os embeddings e salvar como HTML
    visualize_embeddings_tsne(embeddings, labels, save_as_html=True)

    # Plotar gráficos de treinamento
    plot_training_history(history)

if __name__ == "__main__":
    main()
