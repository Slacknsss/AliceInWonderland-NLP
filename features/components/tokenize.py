import re

from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))


def tokenize(text: str) -> list[(str, str)]:
    """
    Tokenize a text

    ## Parameters
        **text**: The text that will be tokenized
        **remove_punct**: Toggle suppression of punctuation in the tokens
        **remove_stop_words**: Toggle suppression of stop words (english stop words)

    ## Returns
        The list of the generated tokens
    """

    if not isinstance(text, str):
        raise TypeError
    elif not text:
        raise ValueError

    return re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
