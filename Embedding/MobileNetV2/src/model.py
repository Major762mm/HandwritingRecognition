import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2  # type: ignore
from tensorflow.keras.models import Model  # type: ignore
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense  # type: ignore

# Função para carregar MobileNetV2 com saída ajustada para 1280 dimensões
def load_mobilenet_embedding_model(num_classes, input_shape=(256, 256, 3)):
    # Carregar MobileNetV2 base
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=input_shape)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)  # Saída de 1280 dimensões (original)
    output = Dense(num_classes, activation='softmax')(x)  # Saída para classificação
    embedding_model = Model(inputs=base_model.input, outputs=output)
    return embedding_model
