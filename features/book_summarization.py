from .components.get_book_content import get_book_content
from .components.clean_book_content import clean_book_content

def summarize_book(book_id: int, book_content: str) -> str:
    """
    Summarize book

    ## Parameters
        **book_id**: Gutenberg project unique identifier
        **book_content**: Book content

    ## Returns
        The summarize of the book
    """

    if (book_content is not None and not isinstance(book_content, str)):
        raise TypeError('book_content must be str')
    elif not isinstance(book_id, int):
        raise TypeError('book_id mut be an int')
    elif book_content is not None and not book_content:
        raise ValueError('book_content need to be fill')
    elif book_id < 0:
        raise ValueError('book_id must be positive')
    
    if book_content is None:
        book_content = get_book_content(book_id)

    if len(book_content) < 750:
        return 'The text is too litle'

    book_content, normalized_book_content = clean_book_content(book_content)

    return {}