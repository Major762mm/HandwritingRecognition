from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

# Carregue embeddings
embeddings = np.load(r'C:\Users\rafael.jose\OneDrive\Documentos\ProjetoBotCity\BotAutom\BotAutom\Embedding\data\embeddings\Paulo Cesar S. - Fiorino 50.npy')

# Verifique o número de amostras
print(f"Número de amostras: {embeddings.shape[0]}")

# Reduza dimensões para 2D com um perplexity menor que o número de amostras
tsne = TSNE(n_components=2, perplexity=5)  # Ajuste perplexity conforme necessário
embeddings_2d = tsne.fit_transform(embeddings)

# Plote as dimensões reduzidas
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
plt.title("t-SNE dos Embeddings")
plt.show()
