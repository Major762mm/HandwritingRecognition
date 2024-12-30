import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity

os.environ["TF_USE_LEGACY_KERAS"] = "1"

# Diretórios
processed_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\processed'
embedding_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\embeddings'
test_image_folder = r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\MobileNetV2\data\TestImage'  # Pasta onde será colocada a imagem de teste

# Função para carregar modelo MobileNetV2
def load_mobilenet_embedding_model(input_shape=(224, 224, 3)):
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=input_shape)
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    embedding_model = Model(inputs=base_model.input, outputs=x)
    return embedding_model

# Função para carregar embeddings previamente salvos
def load_saved_embeddings(embedding_folder):
    embeddings = np.load(os.path.join(embedding_folder, 'embeddings.npy'))
    labels = np.loadtxt(os.path.join(embedding_folder, 'labels.csv'), delimiter=',', dtype=str)
    return embeddings, labels

# Função para carregar imagem de teste e gerar embedding
def generate_test_embedding(model, image_path, target_size=(224, 224)):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img_resized = cv2.resize(img, target_size)
    img_normalized = img_resized / 255.0  # Normalizar imagem
    img_normalized = np.expand_dims(img_normalized, axis=0)  # Expandir dimensão para batch único
    embedding = model.predict(img_normalized)
    return embedding

# Função para comparar embeddings usando similaridade de cosseno
def compare_embeddings_with_threshold(test_embedding, embeddings, labels, threshold=0.8):
    print(f"Dimensão do embedding de teste: {test_embedding.shape}")
    print(f"Dimensão dos embeddings salvos: {embeddings.shape}")

    similarities = cosine_similarity(test_embedding, embeddings)
    most_similar_index = np.argmax(similarities)
    most_similar_label = labels[most_similar_index]
    confidence = similarities[0, most_similar_index]

    if confidence >= threshold:
        return most_similar_label, confidence
    else:
        return "Sem correspondência confiável", confidence

# Função principal para teste de imagens
def test_single_image():
    # Carregar modelo e embeddings salvos
    embedding_model = load_mobilenet_embedding_model()
    embeddings, labels = load_saved_embeddings(embedding_folder)

    # Procurar imagem de teste na pasta
    for filename in os.listdir(test_image_folder):
        if filename.endswith(".png") or filename.endswith(".jpeg"):
            test_image_path = os.path.join(test_image_folder, filename)
            print(f"Testando imagem: {test_image_path}")
            
            # Gerar embedding da imagem de teste
            test_embedding = generate_test_embedding(embedding_model, test_image_path)
            
            # Comparar com embeddings salvos
            predicted_label, confidence = compare_embeddings_with_threshold(test_embedding, embeddings, labels)
            print(f"Resultado: {predicted_label} (Confiança: {confidence:.2f})")
            break
    else:
        print("Nenhuma imagem de teste encontrada na pasta.")

if __name__ == "__main__":
    test_single_image()
