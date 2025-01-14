import os
from utils import load_split_images, save_embeddings
from model import load_mobilenet_embedding_model
from embedding import generate_embeddings
from visul_emb import visualize_embeddings_tsne, plot_training_history
import tensorflow as tf

# Diretórios
split_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\split'
embedding_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\embeddings'
model_save_path = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\mobilenet_v2_model.h5'

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
    train_data = load_split_images(os.path.join(split_folder, 'train'))
    val_data = load_split_images(os.path.join(split_folder, 'val'))
    test_data = load_split_images(os.path.join(split_folder, 'test'))
    # Calcular o número de classes
    num_classes = len(set(map(tuple, train_data[1])))
    from collections import Counter
    import numpy as np
    
    print("Distribuição das classes no conjunto de treinamento:")
    print(Counter(np.argmax(train_data[1], axis=1)))

    print(train_data[1][:50])  # Mostra os primeiros 5 rótulos


    # Verificar se o modelo ajustado já existe
    if os.path.exists(model_save_path):
        print("Carregando modelo salvo...")
        embedding_model = tf.keras.models.load_model(model_save_path)
    else:
        print("Treinando modelo do zero...")
        embedding_model = load_mobilenet_embedding_model(num_classes)
        # Ajuste fino do modelo
        embedding_model, history = fine_tune_mobilenet(embedding_model, train_data, val_data, epochs=10)
        embedding_model.save(model_save_path)  # Salvar modelo ajustado
        # Plotar gráficos de treinamento
        plot_training_history(history)

    # Avaliar no conjunto de teste
    test_images, test_labels = test_data
    test_loss, test_accuracy = embedding_model.evaluate(test_images, test_labels)
    print(f"Avaliação no conjunto de teste - Loss: {test_loss}, Accuracy: {test_accuracy}")

    # Gerar embeddings para os dados de teste
    embeddings = generate_embeddings(embedding_model, test_images)

    # Salvar os embeddings gerados
    save_embeddings(embeddings, test_labels, embedding_folder)

    # Visualizar embeddings com t-SNE e salvar
    # Converter rótulos do formato one-hot para valores únicos
    visualize_embeddings_tsne(embeddings, test_labels, save_as_html=True, output_folder=embedding_folder)

if __name__ == "__main__":
    main()
