from .book_summarization import summarize_book
from .books_similarity import get_books_similarity
from .components.get_book_content import get_book_content
from .components.get_info import get_info
from .components.wordcloud import create_wordcloud
from .lexical_diversity import lexical_diversity


def make_book_card(book_id: int) -> dict[str, dict | list | str]:
    """
    Make book card summary

    ## Parameters
        **book_id**: Gutenberg project unique identifier

    ## Returns
        Book card dictionnary
    """

    if not isinstance(book_id, int):
        raise TypeError('book_id must be int')
    elif book_id < 0:
        raise ValueError

    book_content = get_book_content(book_id)

    book_card = {
        'info': get_info(book_id),
        'lexdiv': lexical_diversity(book_id, book_content),
        'topics': {},
        'entities': {},
        'summary': summarize_book(book_id, book_content),
        'similar': get_books_similarity(book_id, book_content),
    }

    create_wordcloud(
        book_id,
        book_content,
    )

    return book_card
