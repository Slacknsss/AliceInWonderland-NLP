import logging
import re

import nltk
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from .components.get_book_content import get_book_content

Word_Per_Chunk = 1000
N_Topics = 8
N_Words = 9

CHAPTER_PATTERN = re.compile(
    r"(?<!\w)(CHAPTER|CHAP)\s+([IVXLCDM]+|[0-9]+)\.?",
    flags=re.IGNORECASE,
)

LITERARY_STOPWORDS = {
    "said", "could", "would", "should", "upon", "one", "yet", "may",
    "much", "even", "also", "back", "still", "came", "went", "come",
    "like", "know", "little", "great", "man", "men", "time", "hand",
    "good", "mr", "mrs", "miss", "old", "made", "way", "day", "eyes",
    "never", "every", "well", "thought", "looked", "long", "face",
    "us", "without", "always", "away", "thing", "things","oh",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def _build_stopwords():
    nltk.download("stopwords", quiet=True)
    base = set(stopwords.words("english"))
    return list(base | LITERARY_STOPWORDS)


def split_into_chunks(text, words_per_chunk=Word_Per_Chunk):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), words_per_chunk):
        chunk = " ".join(tokens[i:i + words_per_chunk])
        chunks.append(chunk)
    return chunks


def split_book(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    all_boundaries = [m.start() for m in CHAPTER_PATTERN.finditer(text)]

    boundaries = []
    for pos in all_boundaries:
        if not boundaries or pos - boundaries[-1] > 500:
            boundaries.append(pos)

    if len(boundaries) <= 1:
        logger.warning(
            "No chapter markers found — falling back to %d-word chunks.",
            Word_Per_Chunk,
        )
        return split_into_chunks(text)

    chapters = []
    for idx, start in enumerate(boundaries):
        end = boundaries[idx + 1] if idx + 1 < len(boundaries) else len(text)
        chapter_text = text[start:end].strip()
        if chapter_text:
            chapters.append(chapter_text)

    logger.info("Book split into %d segment(s).", len(chapters))
    return chapters

def get_top_words(model, feature_names, n_words):
    topics = []
    for topic in model.components_:
        top_indices = topic.argsort()[-n_words:][::-1]
        words = []
        for i in top_indices:
            words.append(feature_names[i])
        topics.append(words)
    return topics


def extract_topics_from_book(book_id, book_content, n_topics=N_Topics, n_words=N_Words):
    text = book_content
    logger.info("Book fetched for id: %s", book_id)

    chapters = split_book(text)

    vectorizer = CountVectorizer(
        stop_words=_build_stopwords(),
        max_df=0.85,
        min_df=1,
        ngram_range=(1, 2),
        max_features=5000,
    )
    document_term_matrix = vectorizer.fit_transform(chapters)

    actual_n_topics = min(n_topics, len(chapters))
    if actual_n_topics < n_topics:
        logger.warning(
            "Requested %d topics but only %d sections available — using %d topic(s) instead.",
            n_topics,
            len(chapters),
            actual_n_topics,
        )

    lda = LatentDirichletAllocation(
        n_components=actual_n_topics,
        random_state=42,
        learning_method="batch",
        doc_topic_prior=0.1,
        topic_word_prior=0.01,
    )
    lda.fit(document_term_matrix)

    feature_names = vectorizer.get_feature_names_out()
    lda_topics = get_top_words(lda, feature_names, n_words)

    section_topic_matrix = lda.transform(document_term_matrix)
    results = {}
    for i in range(len(chapters)):
        topic_index = section_topic_matrix[i].argmax()
        results[i + 1] = lda_topics[topic_index]
    return results

def topic_modeling(book_id: int, book_content: str | None = None) -> str:
    topics = extract_topics_from_book(
        book_id=book_id,
        book_content=book_content or get_book_content(book_id),
    )

    result = ''

    for section_num, words in topics.items():
        result += f'\n=== Section {section_num} ===\n'
        result += ', '.join(words)
        result += '\n'

    return result
