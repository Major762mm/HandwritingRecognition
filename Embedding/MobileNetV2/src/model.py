from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
import tensorflow as tf
import numpy as np

def load_mobilenet_embedding_model():
    # Carregar o MobileNetV2 pré-treinado
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(128, 128, 3))
    
    # Adicionar uma camada GlobalAveragePooling para embeddings
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    
    # Criar modelo para saída de embeddings
    embedding_model = Model(inputs=base_model.input, outputs=x)
    return embedding_model

def generate_embeddings(model, images):
    # Expandir dimensão para compatibilidade com o modelo
    images_expanded = np.expand_dims(images, axis=-1)  # Para imagens em grayscale
    images_expanded = np.repeat(images_expanded, 3, axis=-1)  # Transformar em RGB

    # Gerar embeddings
    embeddings = model.predict(images_expanded)
    return embeddings
