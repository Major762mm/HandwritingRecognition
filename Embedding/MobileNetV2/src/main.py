import os
from utils import load_split_images, save_embeddings
from model import load_mobilenet_embedding_model
from embedding import generate_embeddings
from visul_emb import visualize_embeddings_tsne, plot_training_history
import tensorflow as tf
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

# Diretórios
split_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\split'
embedding_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\embeddings'
model_save_path = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\mobilenet_v2_model.h5'

# Mapear índices para nomes de classes
class_names = ["forgery", "real", "motorista"]

# Função de treinamento e ajuste fino
def fine_tune_mobilenet(model, train_data, val_data, epochs=10):
    train_images, train_labels = train_data
    val_images, val_labels = val_data

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(
        train_images, train_labels,
        validation_data=(val_images, val_labels),
        epochs=epochs,
        batch_size=16
    )

    return model, history

# Função principal
def main():
    # Carregar imagens dos splits
    train_images, train_labels = load_split_images(os.path.join(split_folder, 'train'))
    val_images, val_labels = load_split_images(os.path.join(split_folder, 'val'))
    test_images, test_labels = load_split_images(os.path.join(split_folder, 'test'))

    # Mostrar número total de imagens carregadas por conjunto
    print(f"\nConjuntos de dados carregados:")
    print(f"Treinamento: {len(train_images)} imagens")
    print(f"Validação: {len(val_images)} imagens")
    print(f"Teste: {len(test_images)} imagens")

    # Calcular o número de classes
    num_classes = len(set(np.argmax(train_labels, axis=1)))
    print(f"Número de classes no conjunto de treinamento: {num_classes}")

    # Mostrar distribuição das classes no conjunto de treinamento
    print("\nDistribuição das classes no conjunto de treinamento:")
    class_distribution = Counter(np.argmax(train_labels, axis=1))
    for class_index, count in class_distribution.items():
        print(f"{class_names[class_index]}: {count} imagens")

    # Exibir algumas imagens com os nomes das classes
    for i in range(5):  # Exibir 5 imagens
        class_index = np.argmax(train_labels[i])  # Índice da classe
        plt.imshow(train_images[i])
        plt.title(f"Classe: {class_names[class_index]}")
        plt.axis('off')  # Remover os eixos para melhor visualização
        plt.show()

    # Verificar se o modelo ajustado já existe
    if os.path.exists(model_save_path):
        print("Carregando modelo salvo...")
        embedding_model = tf.keras.models.load_model(model_save_path)
    else:
        print("Treinando modelo do zero...")
        embedding_model = load_mobilenet_embedding_model(num_classes)
        # Ajuste fino do modelo
        embedding_model, history = fine_tune_mobilenet(
            embedding_model,
            (train_images, train_labels),
            (val_images, val_labels),
            epochs=10
        )
        embedding_model.save(model_save_path)  # Salvar modelo ajustado
        plot_training_history(history)

    # Avaliar no conjunto de teste
    test_loss, test_accuracy = embedding_model.evaluate(test_images, test_labels)
    print(f"\nAvaliação no conjunto de teste - Loss: {test_loss:.4f}, Accuracy: {test_accuracy:.4f}")

    # Gerar embeddings para os dados de teste
    embeddings = generate_embeddings(embedding_model, test_images)

    # Salvar os embeddings gerados
    save_embeddings(embeddings, test_labels, embedding_folder)

    # Visualizar embeddings com t-SNE e salvar
    visualize_embeddings_tsne(embeddings, test_labels, save_as_html=True, output_folder=embedding_folder)

if __name__ == "__main__":
    main()
