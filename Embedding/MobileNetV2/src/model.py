import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2 # type: ignore
from tensorflow.keras.models import Model # type: ignore
import numpy as np
import os

os.environ["TF_USE_LEGACY_KERAS"] = "1"
# pylint: disable=wrong-import-position

def load_mobilenet_embedding_model():
    # Carregar o MobileNetV2 pré-treinado
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(256, 256, 1))
    
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

def fine_tune_mobilenet(model, images, labels, epochs=5):
    # Congelar as camadas iniciais do modelo
    for layer in model.layers[:-10]:  # Descongela as últimas 10 camadas
        layer.trainable = False

    # Compilar o modelo para treino
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Transformar rótulos em one-hot encoding
    from sklearn.preprocessing import LabelBinarizer
    lb = LabelBinarizer()
    labels_one_hot = lb.fit_transform(labels)

    # Treinar o modelo com seus dados
    model.fit(images, labels_one_hot, epochs=epochs, batch_size=16)

    return model
