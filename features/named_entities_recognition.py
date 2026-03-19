#ma fonction a besoin de faire 4 chose:
#- Lire le fichier texte du Livre 
#- Passer le texte a spacy pour trouver les string de localisaiton 
#-Filtrer les entitées par label( PERSON,GPE,LOC)
#-Retourner le dictionnaire exemple : {"characteres" : [JEAN], "locations":[PARIS]}

import spacy
nlp = spacy.load("en_core_web_md")# chargement du model (il sait reconnaitre les mots, les types ,les entitiés )
def named_entities(book_id):
    with open(f"{book_id}.txt", "r") as f:
        text = f.read()
    
    characters = set()
    locations = set()
    chunk_size = 10000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

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
