from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import normalize

# Carregue embeddings
try:
    embeddings = np.load(r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\embeddings\Paulo Cesar S. - Fiorino 50.npy')

    # Verifique o número de amostras
    print(f"Número de dimensões dos embeddings: {embeddings.shape}")
    
    # Caso seja uma única amostra, ajuste para evitar erros
    if len(embeddings.shape) == 1:
        embeddings = embeddings.reshape(1, -1)
    
    if embeddings.shape[0] <= 5:
        print("Aviso: Número de amostras muito pequeno para t-SNE. Resultados podem não ser representativos.")
    
    # Normalize os embeddings
    embeddings = normalize(embeddings, norm='l2')  # Normaliza com norma L2
    print("Embeddings normalizados.")
    
    # Reduza dimensões para 2D com t-SNE
    tsne = TSNE(n_components=2, perplexity=min(30, embeddings.shape[0] - 1), random_state=42)
    embeddings_2d = tsne.fit_transform(embeddings)
    print("t-SNE concluído.")
    
    # Plote as dimensões reduzidas
    plt.figure(figsize=(8, 8))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
    plt.title("t-SNE dos Embeddings")
    plt.xlabel("Dimensão 1")
    plt.ylabel("Dimensão 2")
    plt.grid(True)
    plt.show()

except Exception as e:
    print(f"Erro ao carregar ou processar os embeddings: {e}")