from components.get_book_content import get_book_content
from components.tokenize import tokenize

def lexical_diversity(book_id: int) -> dict[str, int|float]:
    """
    
    """

    book_content = get_book_content(book_id)
    tokens = tokenize(text=book_content, remove_punct=True, remove_stop_words=True)
    
    tok = len(tokens)
    typ = len(set(tokens))
    hap = len([token for token in tokens if tokens.count(token) == 1])
    ttr = typ / tok
    mwl = sum([len(word[0]) for word in tokens]) / tok
    mwf = tok / typ

    result = {
        'tok': tok, # total number of word tokens
        'typ': typ, # number of unique word tokens
        'hap': hap, # number of word tokens occurring only once
        'ttr': ttr, # number of unique words tokens divided by number of word tokens
        'mwl': mwl, # mean number of characters per word token
        'mwf': mwf # number of word token divided by number of unique word tokens
    }

    print(result)
    return result