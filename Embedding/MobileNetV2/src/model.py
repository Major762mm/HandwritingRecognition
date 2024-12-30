import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense

# Função para carregar MobileNetV2 com ajuste fino
def load_mobilenet_embedding_model(num_classes, input_shape=(256, 256, 3)):
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=input_shape)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)  # Adiciona camada intermediária
    output = Dense(num_classes, activation='softmax')(x)  # Saída para classificação
    embedding_model = Model(inputs=base_model.input, outputs=output)
    return embedding_model
