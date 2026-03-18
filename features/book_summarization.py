from .components.get_book_content import get_book_content

def summarize_book(book_content: str) -> str:
    """
    Summarize book

    ## Parameters
        **book_content**: Book content

    ## Returns
        The summarize of the book
    """

    if not isinstance(book_content, str):
        raise TypeError('book_content must be str')
    elif not book_content:
        raise ValueError('empty book')

    return {}