import re
import argparse
import logging
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from components.download import download_book
from components.remove_gutenberg_tags import remove_gutenberg_tags

Word_Per_Chunk = 2000
N_Topics = 10
N_Words = 10

CHAPTER_PATTERN = re.compile(
    r"\n\s*(CHAPTER|Chapter|CHAP|Chap|BOOK|Book)\s+([IVXLC0-9]+|\w+)[^\n]*\n",
    flags=re.IGNORECASE,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def split_into_chunks(text, words_per_chunk=Word_Per_Chunk):
    tokens = text.split()
    chunks = []

    for i in range(0, len(tokens), words_per_chunk):
        chunk = " ".join(tokens[i:i + words_per_chunk])
        chunks.append(chunk)

    return chunks


def split_book(text):
    text = text.replace("\r\n", "\n")  # amélioration robustesse
    text = re.sub(r"\n{3,}", "\n\n", text)  # amélioration robustesse
    text = text.strip()  # amélioration robustesse

    parts = re.split(CHAPTER_PATTERN, text)

    chapters = []
    buffer = ""

    for part in parts:
        if CHAPTER_PATTERN.match(part):
            if buffer.strip():
                chapters.append(buffer.strip())
            buffer = part
        else:
            buffer += part

    if buffer.strip():
        chapters.append(buffer.strip())

    if len(chapters) <= 1:
        logger.warning(
            "No chapter markers found — falling back to %d-word chunks.",
            Word_Per_Chunk,
        )
        chapters = split_into_chunks(text)

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


def extract_topics_from_book(book_id, n_topics=N_Topics, n_words=N_Words):

    path = download_book(book_id)
    logger.info("Book downloaded to: %s", path)

    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()

    text = remove_gutenberg_tags(text)

    chapters = split_book(text)

    vectorizer = CountVectorizer(
        stop_words="english",
        max_df=0.9,
        min_df=2,
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


def _build_parser():

    parser = argparse.ArgumentParser(
        description="Extract main topics from each section of a Project Gutenberg book.",
    )

    parser.add_argument(
        "--topics",
        type=int,
        required=True,
        help="Numeric book ID from Project Gutenberg.",
    )

    return parser


def main():

    nltk.download("punkt", quiet=True)

    parser = _build_parser()
    args = parser.parse_args()

    topics = extract_topics_from_book(
        book_id=args.topics,
    )

    for section_num, words in topics.items():
        print(f"\n=== Section {section_num} ===")
        print(", ".join(words))


if __name__ == "__main__":
    main()