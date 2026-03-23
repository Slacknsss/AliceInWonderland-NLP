## Named Entities Recognition

Cette feature identifie les personnages et lieux mentionnés dans un livre.

### Approches testées

#### Version 1 — NLTK (sans modèle)
Une première version a été développée avec `nltk` uniquement, sans modèle lourd :
```python
from nltk import ne_chunk, pos_tag, word_tokenize
tree = ne_chunk(pos_tag(word_tokenize(chunk)))
```
**Résultat** : moins précis — beaucoup de faux positifs comme `'Fury'`, `'Soup'`, `'Mystery'` détectés comme personnages. Abandonné au profit de spaCy.

#### Version 2 — spaCy `en_core_web_md` (version finale)
Plus précis et toujours considéré comme un modèle léger.

---

### Raisonnement ligne par ligne

#### 1. Chargement du modèle
```python
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")
```
On tente de charger le modèle spaCy. S'il n'est pas installé sur la machine (`OSError`), on le télécharge automatiquement avant de le recharger. Cela garantit que le programme tourne **sur n'importe quelle machine** sans configuration manuelle.

#### 2. Récupération du contenu du livre
```python
book_content = book_content or get_book_content(book_id)
```
Si le contenu du livre est déjà fourni, on l'utilise directement. Sinon, on le télécharge via `get_book_content`. Cela évite de télécharger le livre plusieurs fois si on enchaîne plusieurs features.

#### 3. Découpage en chunks
```python
chunk_size = 10000
chunks = [book_content[i:i+chunk_size] for i in range(0, len(book_content), chunk_size)]
```
Un livre entier peut faire 150 000+ caractères. Passer tout le texte d'un coup à spaCy serait lent et consommerait beaucoup de mémoire. On découpe donc en morceaux de 10 000 caractères traités un par un.

#### 4. Utilisation de `set()` au lieu de `list()`
```python
characters = set()
locations = set()
```
Un `set` ne peut pas contenir de doublons — `Alice` apparaît des centaines de fois dans le livre, mais ne sera ajoutée qu'une seule fois. Plus efficace que de filtrer les doublons après coup avec `list(set(...))`.

#### 5. Filtrage des entités
```python
for ent in doc.ents:
    if ent.label_ == "PERSON" and "\n" not in ent.text and not ent.text.startswith("CHAPTER"):
        characters.add(ent.text)
    elif ent.label_ in ["GPE", "LOC"] and "\n" not in ent.text:
        locations.add(ent.text)
```
- `ent.label_ == "PERSON"` → filtre les personnages
- `"\n" not in ent.text` → élimine les titres de chapitres mal détectés comme `"CHAPTER I.\nDown"`
- `not ent.text.startswith("CHAPTER")` → filtre supplémentaire pour les chapitres
- `ent.label_ in ["GPE", "LOC"]` → `GPE` = lieux géopolitiques (pays, villes), `LOC` = lieux physiques

#### 6. Retour du dictionnaire
```python
return {
    "characters": list(characters),
    "locations": list(locations)
}
```
On convertit les `set` en `list` car le format de retour attendu est une liste de strings.

---

### Pipeline
```
Texte brut → Découpage en chunks → spaCy NER → Filtrage par label → Dictionnaire
```

### Retourne
```python
{
    "characters": ["Alice", "Queen", ...],
    "locations": ["London", "Wonderland", ...]
}
```
