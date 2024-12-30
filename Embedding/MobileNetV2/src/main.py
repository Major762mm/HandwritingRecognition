import os
from utils import load_processed_images, save_embeddings
from model import load_mobilenet_embedding_model
from embeddings import generate_embeddings
from visualization import visualize_embeddings_tsne, plot_training_history
import tensorflow as tf
from sklearn.preprocessing import LabelBinarizer

# Diretórios
processed_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\processed'
embedding_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\embeddings'

# Função de treinamento e ajuste fino
def fine_tune_mobilenet(model, images, labels, epochs=5):
    lb = LabelBinarizer()
    labels_one_hot = lb.fit_transform(labels)
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(images, labels_one_hot, epochs=epochs, batch_size=16)
    
    return model, history

# Função principal
def main():
    # Carregar imagens e rótulos
    images, labels = load_processed_images(processed_folder)
    num_classes = len(set(labels))  # Número de classes
    print(f"Número de classes: {num_classes}")
    
    # Carregar e ajustar o modelo MobileNetV2
    embedding_model = load_mobilenet_embedding_model(num_classes)
    
    # Ajuste fino do modelo
    embedding_model, history = fine_tune_mobilenet(embedding_model, images, labels, epochs=10)
    
    # Gerar embeddings para as imagens
    embeddings = generate_embeddings(embedding_model, images)
    
    # Salvar os embeddings gerados
    save_embeddings(embeddings, labels, embedding_folder)
    
    # Visualizar embeddings com t-SNE e salvar
    visualize_embeddings_tsne(embeddings, labels, save_as_html=True, output_folder=embedding_folder)
    
    # Plotar gráficos de treinamento
    plot_training_history(history)

if __name__ == "__main__":
    main()
