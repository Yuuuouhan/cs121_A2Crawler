# import contractions
import re

# have a file of stop words

tokens = []

def tokenize(text):
    """
    Tokenizes the given text string.
    Parameters:
    text (str): The text string to be tokenized.
    Returns:
    list: A list of tokens (words) extracted from the text string.
    Time Complexity: O(n), where n is the number of characters in the text string.
    """
    pattern = r'\b\w+\b'
    lowercase_text = text.lower()
    words = re.findall(pattern, lowercase_text)
    tokens.extend(words)
    return tokens

def compute_word_frequencies(tokens):
    """
    Computes the frequency of each word in the list of tokens.
    Parameters:
    tokens (list): A list of tokens (words).
    Returns:
    defaultdict: A dictionary with words as keys and their frequencies as values.
    Time Complexity: O(n), where n is the number of tokens.
    """
    word_frequencies = {}
    for token in tokens:
        if token in word_frequencies:
            word_frequencies[token] += 1
        else:
            word_frequencies[token] = 1  
    return word_frequencies

