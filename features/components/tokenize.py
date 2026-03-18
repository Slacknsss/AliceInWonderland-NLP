import string
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def tokenize(text: str, remove_punct: bool=False, remove_stop_words: bool=False) -> list[(str, str)]:
    """
    Tokenize a text

    # Parameters
        **text**: The text that will be tokenized
        **remove_punct**: Toggle suppression of punctuation in the tokens
        **remove_stop_words**: Toggle suppression of stop words (english stop words)
    
    # Returns
        The list of the generated tokens
    """

    if not isinstance(text, str) or not isinstance(remove_punct, bool) or not isinstance(remove_stop_words, bool):
        raise TypeError
    elif not text:
        raise ValueError

    tokenized = [
        word for word in tokenized 
        if word not in (remove_stop_words and stop_words or [])
    ]

    if remove_punct:
        for i in range(len(tokenized)):
            for character in string.punctuation:
                tokenized[i] = tokenized[i].replace(character, '')

    return tokenized