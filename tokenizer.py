import re

# account for contractions, non-enlish tokens, single-letter tokens

tokens_dict = {}

def tokenize(text: str) -> None:
    """
    Tokenizes the given text string, and updates all tokens in tokens_dict.

    @param text: a string that needs to be tokenized.
    @return: None
    """
    pattern = r'\W+'
    lowercase_text = text.lower()
    words = re.findall(pattern, lowercase_text)
    for word in words:
        if word in tokens_dict:
            tokens_dict[word] += 1
        else:
            tokens_dict[word] == 1

def compute_word_frequencies() -> dict:
    """
    Returns the 50 most common tokens in tokens_dict based on frequency.

    @return: dictionary of the 50 most common words and their frequencies, in order.
    """
    return dict(sorted(tokens_dict.items(), key=lambda x: x[1]))

if __name__ == "__main__":
    sample_string = "is This this is a sample tesTing string. It contains some test words. It's a test. ಹಲೋ, ಹೇಗಿದ್ದೀಯನ್ನು ಕಾರ್ಯಕ"
    tokenize(sample_string)
    print(compute_word_frequencies())