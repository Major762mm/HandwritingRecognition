import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
from sklearn.metrics.pairwise import cosine_similarity

# Configuração para compatibilidade com versões específicas do TensorFlow
os.environ["TF_USE_LEGACY_KERAS"] = "1"

# Diretórios
embedding_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\embeddings'
test_image_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\TestImage'
saved_model_path = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\mobilenet_v2_model.h5'

# Função para carregar o modelo salvo
def load_trained_model(saved_model_path):
    if not os.path.exists(saved_model_path):
        raise FileNotFoundError(f"Modelo salvo não encontrado em: {saved_model_path}")
    model = load_model(saved_model_path)
    print("Modelo carregado com sucesso.")
    return model

# Função para carregar embeddings salvos
def load_saved_embeddings(embedding_folder):
    embeddings_path = os.path.join(embedding_folder, 'embeddings.npy')
    labels_path = os.path.join(embedding_folder, 'labels.csv')

    if not os.path.exists(embeddings_path) or not os.path.exists(labels_path):
        raise FileNotFoundError("Embeddings ou labels não encontrados.")

    embeddings = np.load(embeddings_path)
    labels = np.loadtxt(labels_path, delimiter=',', dtype=str)
    print(f"Dimensão dos embeddings carregados: {embeddings.shape}")
    return embeddings, labels

# Função para gerar embedding de uma imagem de teste
def generate_test_embedding(model, image_path, target_size=(256, 256)):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Erro ao carregar a imagem: {image_path}")
    
    img_resized = cv2.resize(img, target_size)
    img_normalized = img_resized / 255.0
    img_normalized = np.expand_dims(img_normalized, axis=0)  # Expandir dimensão para batch único
    embedding = model.predict(img_normalized)
    print(f"Dimensão do embedding gerado: {embedding.shape}")
    return embedding

# Função para comparar embeddings usando similaridade de cosseno
def compare_embeddings_with_threshold(test_embedding, embeddings, labels, threshold=0.8):
    if test_embedding.shape[1] != embeddings.shape[1]:
        raise ValueError(
            f"Dimensões incompatíveis: test_embedding.shape[1]={test_embedding.shape[1]} "
            f"enquanto embeddings.shape[1]={embeddings.shape[1]}"
        )

    similarities = cosine_similarity(test_embedding, embeddings)
    most_similar_index = np.argmax(similarities)
    most_similar_label = labels[most_similar_index]
    confidence = similarities[0, most_similar_index]

    if confidence >= threshold:
        return most_similar_label, confidence
    else:
        return "Sem correspondência confiável", confidence

# Função principal para testar uma única imagem
def test_single_image():
    # Carregar o modelo salvo e os embeddings salvos
    trained_model = load_trained_model(saved_model_path)
    embeddings, labels = load_saved_embeddings(embedding_folder)

    # Procurar imagem de teste na pasta
    test_images = [f for f in os.listdir(test_image_folder) if f.lower().endswith(('.png', '.jpeg', '.jpg'))]
    if not test_images:
        print("Nenhuma imagem de teste encontrada na pasta.")
        return

    for filename in test_images:
        test_image_path = os.path.join(test_image_folder, filename)
        print(f"Testando imagem: {test_image_path}")

        try:
            # Gerar embedding da imagem de teste
            test_embedding = generate_test_embedding(trained_model, test_image_path)

            # Garantir que as dimensões sejam consistentes
            test_embedding = np.squeeze(test_embedding)
            embeddings = np.array(embeddings)

            if test_embedding.ndim == 1:
                test_embedding = test_embedding.reshape(1, -1)
            if embeddings.ndim == 1:
                embeddings = embeddings.reshape(1, -1)

            # Comparar com embeddings salvos
            predicted_label, confidence = compare_embeddings_with_threshold(test_embedding, embeddings, labels)
            print(f"Resultado: {predicted_label} (Confiança: {confidence:.2f})")
        except Exception as e:
            print(f"Erro ao testar a imagem {filename}: {e}")

if __name__ == "__main__":
    test_single_image()
