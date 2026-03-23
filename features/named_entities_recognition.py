# ma fonction a besoin de faire 4 chose:
# - Lire le fichier texte du Livre
# - Passer le texte a spacy pour trouver les string de localisaiton
# -Filtrer les entitées par label( PERSON,GPE,LOC)
# -Retourner le dictionnaire exemple : {"characteres" : [JEAN], "locations":[PARIS]}
import spacy
from spacy.cli import download

from .components.get_book_content import get_book_content

try:
    nlp = spacy.load("en_core_web_md")  # chargement du model (il sait reconnaitre les mots, les types ,les entitiés )
except OSError:
    download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")

def named_entities(book_id: int, book_content: str | None = None) -> dict[str, list]:
    """
    Identify characters and locations mentioned in the book

    ## Parameters
        **book_id**: Gutenberg project unique identifier
        **book_content**: Book content

    ## Returns
        Dictionnary with list of characters and locations
    """

    book_content = book_content or get_book_content(book_id)
    characters = set()
    locations = set()
    chunk_size = 10000
    chunks = [book_content[i:i+chunk_size] for i in range(0, len(book_content), chunk_size)]

    for chunk in chunks:
        doc = nlp(chunk)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and "\n" not in ent.text and not ent.text.startswith("CHAPTER"):
                characters.add(ent.text)
            elif ent.label_ in ["GPE", "LOC"] and "\n" not in ent.text :
                locations.add(ent.text)
    return {
        "characters": list(characters),
        "locations": list(locations)
    }
