from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import os 
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
texts = []
for fichier in os.listdir('alice_assets/books/'):
    if fichier.endswith('.txt'):
        with open(f'alice_assets/books/{fichier}') as f:
            text =f.read()
            texts.append(text)

vectorizer = TfidfVectorizer(max_features= 1000, stop_words="english")
X = vectorizer.fit_transform(texts)
kMeans = KMeans(n_clusters=3, random_state=42)
kMeans.fit(X)
print(kMeans.labels_)
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X.toarray())
# Noms des fichiers pour les labels
titres = [f for f in os.listdir('alice_assets/books/') if f.endswith('.txt')]

# Affichage
colors = ["red", "blue", "green"]
plt.figure(figsize=(10, 6))
for i, (titre, label) in enumerate(zip(titres, kMeans.labels_)):
    plt.scatter(X_2d[i, 0], X_2d[i, 1], color=colors[label], s=100)
    plt.annotate(titre, (X_2d[i, 0], X_2d[i, 1]), fontsize=8)

plt.title("Clustering des livres")
plt.savefig("alice_assets/plots/clustering.png")
plt.show()