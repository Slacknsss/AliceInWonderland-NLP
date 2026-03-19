from .components.get_book_content import get_book_content

def get_books_similarity(book_id: int, book_content: str) -> list[str]:
    """
    Get similar books

    ## Parameters
        **book_id**: Gutenberg project unique identifier
        **book_content**: Book content

    ## Returns
        List of the 5 best recommendations based on similarity
    """

    similar_books = []


    return similar_books