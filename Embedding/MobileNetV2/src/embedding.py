import numpy as np

# Função para gerar embeddings
def generate_embeddings(model, images):
    embeddings = model.predict(images)
    return embeddings
