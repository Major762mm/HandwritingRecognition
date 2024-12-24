from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

def visualize_embeddings_tsne(embeddings, labels):
    tsne = TSNE(n_components=2, perplexity=30, n_iter=5000)
    embeddings_2d = tsne.fit_transform(embeddings)
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=labels, cmap="tab10")
    plt.colorbar(scatter)
    plt.title("t-SNE dos Embeddings")
    plt.xlabel("Dimensão 1")
    plt.ylabel("Dimensão 2")
    plt.show()
