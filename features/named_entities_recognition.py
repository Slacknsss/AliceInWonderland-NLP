# ma fonction a besoin de faire 4 chose:
# - Lire le fichier texte du Livre
# - Passer le texte a spacy pour trouver les string de localisaiton
# -Filtrer les entitées par label( PERSON,GPE,LOC)
# -Retourner le dictionnaire exemple : {"characteres" : [JEAN], "locations":[PARIS]}
import spacy

nlp = spacy.load(
    'en_core_web_md'
)  # chargement du model (il sait reconnaitre les mots, les types ,les entitiés )


def named_entities(book_id):
    with open(f'{book_id}.txt') as f:
        text = f.read()
    doc = nlp(text)
    characters = []
    locations = []
    for entities in doc.ents:
        if entities.label_ == 'PERSON' and '\n' not in entities.text:
            characters.append(entities.text)
        elif entities.label_ in ['GPE', 'LOC']:
            locations.append(entities.text)
    return {'characters': list(set(characters)), 'locations': list(set(locations))}
