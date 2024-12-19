from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

# Carregue embeddings
embeddings = np.load('data/embeddings/Paulo Cesar S. - Fiorino 50.npy')

# Reduza dimensões para 2D
tsne = TSNE(n_components=2)
embeddings_2d = tsne.fit_transform(embeddings)

# Plote as dimensões reduzidas
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
plt.title("t-SNE dos Embeddings")
plt.show()
