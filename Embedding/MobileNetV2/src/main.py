import tensorflow as tf
from prep import preprocess_images
from model import load_mobilenet_embedding_model, generate_embeddings
from dimemb import visualize_embeddings_tsne
# 1. Pré-processamento das imagens
image_folder = "caminho/para/dataset"
images, labels = preprocess_images(image_folder)

# 2. Carregar modelo de embeddings
embedding_model = load_mobilenet_embedding_model()

# 3. Gerar embeddings
embeddings = generate_embeddings(embedding_model, images)

# 4. Visualizar embeddings
visualize_embeddings_tsne(embeddings, labels)