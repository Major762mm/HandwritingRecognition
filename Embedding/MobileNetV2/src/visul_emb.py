import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# Função para visualizar embeddings com t-SNE
import numpy as np
import plotly.express as px
from sklearn.manifold import TSNE

def visualize_embeddings_tsne(embeddings, labels, save_as_html=False, output_folder=None):
    # Verificar se os rótulos estão em formato one-hot encoding e converter se necessário
    if len(labels.shape) > 1 and labels.shape[1] > 1:  # Verifica se é 2D (one-hot)
        labels = np.argmax(labels, axis=1)  # Converte para rótulos únicos
    
    # Reduzir a dimensionalidade dos embeddings para 2D usando t-SNE
    tsne = TSNE(n_components=2, perplexity=30, n_iter=5000, random_state=42)
    embeddings_2d = tsne.fit_transform(embeddings)

    # Criar gráfico de dispersão interativo
    fig = px.scatter(
        x=embeddings_2d[:, 0],
        y=embeddings_2d[:, 1],
        color=labels,
        title="t-SNE dos Embeddings (Gráfico Interativo)",
        labels={"x": "Dimensão 1", "y": "Dimensão 2", "color": "Rótulos"}
    )
    
    # Salvar ou exibir o gráfico
    if save_as_html:
        if output_folder is None:
            raise ValueError("O parâmetro 'output_folder' deve ser especificado quando 'save_as_html=True'.")
        output_path = f"{output_folder}/resultado_tsne.html"
        fig.write_html(output_path)
        print(f"Gráfico interativo salvo como '{output_path}'. Abra-o no navegador.")
    else:
        fig.show()


# Função para plotar gráficos de treinamento
def plot_training_history(history):
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    axs[0].plot(history.history['loss'], label='Perda')
    axs[0].set_title('Perda ao Longo das Épocas')
    axs[0].set_xlabel('Épocas')
    axs[0].set_ylabel('Perda')
    axs[0].legend()

    axs[1].plot(history.history['accuracy'], label='Precisão')
    axs[1].set_title('Precisão ao Longo das Épocas')
    axs[1].set_xlabel('Épocas')
    axs[1].set_ylabel('Precisão')
    axs[1].legend()

    plt.tight_layout()
    plt.show()
