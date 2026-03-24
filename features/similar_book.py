import argparse

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from .components.get_book_content import get_book_content
except ImportError:
    from components.get_book_content import get_book_content

N_SIMILAR = 5

BOOK_COLLECTION = {
    11:    "Alice's Adventures in Wonderland",
    12:    "Through the Looking-Glass",
    16:    "Peter Pan",
    55:    "The Wonderful Wizard of Oz",
    113:   "The Secret Garden",
    120:   "Treasure Island",
    236:   "The Jungle Book",
    108:   "The Return of Sherlock Holmes",
    834:   "The Memoirs of Sherlock Holmes",
    863:   "The Mysterious Affair at Styles",
    1661:  "The Adventures of Sherlock Holmes",
    61262: "Poirot Investigates",
    69087: "The Murder of Roger Ackroyd",
    70114: "The Big Four",
    35:    "The Time Machine",
    36:    "The War of the Worlds",
    84:    "Frankenstein; Or, The Modern Prometheus",
    159:   "The Island of Doctor Moreau",
    164:   "Twenty Thousand Leagues under the Sea",
    345:   "Dracula",
}

LITERARY_STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'of', 'to', 'in', 'on', 'at', 'for', 'with', 'by', 'is', 'are', 'was',
    'were', 'be', 'been', 'it', 'this', 'that', 'these', 'those', 'as', 'from', 'not', 'he', 'she', 'they', 'we',
    'you', 'i', 'his', 'her', 'their', 'our', 'my', 'your', 'him', 'them', 'me', 'us', 'do', 'did', 'does', 'have',
    'has', 'had', 'so', 'if', 'then', 'than', 'into', 'out', 'up', 'down', 'all', 'any', 'what', 'which', 'who', 'whom',
    'when', 'where', 'why', 'how', 'can', 'could', 'would', 'should', 'shall', 'will', 'may', 'might', 'must', 'there',
    'here', 'too', 'very', 'just', 'about', 'over', 'under', 'again', 'once',
}


def build_stopwords():
    """
    Build the list of stopwords used by the vectorizer.

    It combines the default NLTK English stopwords with stopwords
    defined in the project.

    ## Parameters
        None

    ## Returns
        A list containing all stopwords used for text preprocessing
    """
    nltk.download('stopwords', quiet=True)
    base = set(stopwords.words('english'))
    return list(base | LITERARY_STOPWORDS)


def load_all_books(book_ids: list):
    """
    Download and return the raw text for each book in the collection.

    Books that fail to download are silently skipped so that one
    unavailable title does not abort the whole process.

    ## Parameters
        **book_ids**: list of Project Gutenberg identifiers to fetch

    ## Returns
        A tuple (ids, texts) where ids is the filtered list of book
        identifiers that were successfully downloaded and texts is the
        corresponding list of raw book contents
    """
    ids = []
    texts = []

    for book_id in book_ids:
        content = get_book_content(book_id)
        if content:
            ids.append(book_id)
            texts.append(content)

    return ids, texts


def vectorize_books(texts: list):
    """
    Transform a list of book texts into a TF-IDF matrix.

    TfidfVectorizer combines CountVectorizer and TfidfTransformer into a
    single step.

    The fitted vectorizer is returned so that any new text can later be projected 
    into the same vector space using transform() instead of fit_transform().

    ## Parameters
        **texts**: list of raw book contents

    ## Returns
        A tuple (tfidf_matrix, vectorizer) where tfidf_matrix is a 
        matrix of shape (n_books, n_features) and vectorizer is the fitted TfidfVectorizer
    """
    vectorizer = TfidfVectorizer(
        stop_words=build_stopwords(),
        max_df=0.85,
        min_df=1,
        ngram_range=(1, 2),
        max_features=5000,
    )
    tfidf_matrix = vectorizer.fit_transform(texts)

    return tfidf_matrix, vectorizer

