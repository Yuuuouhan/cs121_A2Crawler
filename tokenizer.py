import re
from itertools import islice
import contractions

# account for single-letter tokens

tokens_dict = {}

def tokenize(text: str) -> list:
    """
    Tokenizes the given text string, and updates all tokens in tokens_dict.

    @param text: a string that needs to be tokenized.
    @return: None
    """
    try:
        pattern = r'[^a-zA-Z0-9_]'
        lowercase_text = contractions.fix(text.lower())
        words = re.sub(pattern, " ", lowercase_text).split(" ")
        with open("stop_words.txt", 'r', encoding='utf-8') as file:
            forbidden_words = set(file.read().split())
            filtered_list = [word for word in words if word not in forbidden_words]
        for word in filtered_list:
            if word in tokens_dict and word != ' ' and word != '':
                tokens_dict[word] += 1
                print(word)
            elif word != ' ' and word != '':
                tokens_dict[word] = 1
                print(word)
        return words
    except KeyError:
        pass

def compute_word_frequencies() -> dict:
    """
    Returns the 50 most common tokens in tokens_dict based on frequency.

    @return: dictionary of the 50 most common words and their frequencies, in order.
    """
    sorted_dict = dict(sorted(tokens_dict.items(), key=lambda x: (-x[1], x[0])))
    return dict(islice(sorted_dict.items(), 50))