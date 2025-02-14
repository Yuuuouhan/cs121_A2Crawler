import re

# account for contractions, non-enlish tokens, single-letter tokens

tokens_dict = {}

def tokenize(text: str) -> None:
    """
    Tokenizes the given text string, and updates all tokens in tokens_dict.

    @param text: a string that needs to be tokenized.
    @return: None
    """
    try:
        pattern = r'[^a-zA-Z0-9_]'
        lowercase_text = text.lower()
        words = re.sub(pattern, " ", lowercase_text).split(" ")
        for word in words:
            if word in tokens_dict and word != ' ' and word != '':
                tokens_dict[word] += 1
            elif word != ' ' and word != '':
                tokens_dict[word] = 1
        return words
    except KeyError:
        pass

def compute_word_frequencies() -> dict:
    """
    Returns the 50 most common tokens in tokens_dict based on frequency.

    @return: dictionary of the 50 most common words and their frequencies, in order.
    """
    return dict(sorted(tokens_dict.items(), key=lambda x: (-x[1], x[0])))