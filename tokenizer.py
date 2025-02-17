import re
from itertools import islice
import contractions

tokens_dict = {}


def current_tokens(text:str) -> list:
    """
    Tokenizes the current set of tokens going through the current website being processed.

    @param text: a string that needs to be tokenized.
    @return: list of tokens.
    """
    try:
        pattern = r'[^a-zA-Z0-9_]'
        lowercase_text = contractions.fix(text.lower())
        words = re.sub(pattern, " ", lowercase_text).split(" ")
        with open("stop_words.txt", 'r', encoding='utf-8') as file:
            forbidden_words = set(file.read().split())
            filtered_list = [word for word in words if word not in forbidden_words]
        return filtered_list
    except KeyError:
        pass

def current_word_frequencies(tokens_list: list) -> dict:
    """
    Takes the current tokens being processed and returns a frequency dictionary of them.

    @param: tokens that are in the current website.
    @return: their frequencies
    """
    frequency_dict = {}
    for word in tokens_list:
        if word in tokens_dict and word != ' ' and word != '':
            frequency_dict[word] += 1
        elif word != ' ' and word != '':
            frequency_dict[word] = 1
    return frequency_dict

def update_tokens_dict(tokens_list: list) -> None:
    """
    Takes the current tokens returned from current_tokens and adds the tokens to the global
    token frequency dictionary.

    @param: tokens that are in the current website.
    @return: None
    """
    for word in tokens_list:
        if word in tokens_dict and word != ' ' and word != '':
            tokens_dict[word] += 1
        elif word != ' ' and word != '':
            tokens_dict[word] = 1

def compute_word_frequencies() -> dict:
    """
    Copy + paste compute_word_frequencies().

    @return: dictionary of the 50 most common words and their frequencies, in order.
    """
    sorted_dict = dict(sorted(tokens_dict.items(), key=lambda x: (-x[1], x[0])))
    return dict(islice(sorted_dict.items(), 50))