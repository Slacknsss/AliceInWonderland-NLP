from collections import Counter

from .components.get_book_content import get_book_content
from .components.tokenize import tokenize

def lexical_diversity(book_id: int) -> dict[str, int|float]:
    """
    Get lexical informations about a book based on tokenization

    ## Parameters
        **book_id**: Book guternberg unique identifier

    ## Returns
        Dictionnary with lexical diversity metrics :
        
        "tok":int, # total number of word tokens
        "typ":int, # number of unique word tokens
        "hap":int, # number of word tokens occurring only once
        "ttr":float, # number of unique words tokens divided by number of word tokens
        "mwl":float, # mean number of characters per word token
        "mwf":float # number of word token divided by number of unique word tokens
    """

    book_content = get_book_content(book_id)
    tokens = tokenize(text=book_content, remove_punct=True, remove_stop_words=True)

    tok = len(tokens)
    counts = Counter(tokens)
    typ = len(counts)
    hap = sum(1 for count in counts.values() if count == 1)
    ttr = typ / tok
    mwl = sum([len(word) for word in tokens]) / tok
    mwf = tok / typ

    result = {
        'tok': tok, # total number of word tokens
        'typ': typ, # number of unique word tokens
        'hap': hap, # number of word tokens occurring only once
        'ttr': ttr, # number of unique words tokens divided by number of word tokens
        'mwl': mwl, # mean number of characters per word token
        'mwf': mwf # number of word token divided by number of unique word tokens
    }

    return result