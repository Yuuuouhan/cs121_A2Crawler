# import contractions
import re

# have a file of stop words

tokens = []

# def tokenize(content: str) -> list:
#     """
# 	Takes a string of content, returns a list of viable tokens in the string.
	
# 	@param content: string of content.
# 	@return: list of nonunique tokens
# 	"""
#     tokens_list = []
#     try:
# 		# words = contractions.fix(content.lower()).split()
#         words = content.lower().split()
#         for word in words:
#             if '-' in word:
#                 word_separate = word.split('-')
#                 words.append(str(word_separate))
#                 continue
#             word = re.sub(r'[^a-z0-9]', " ", word)
#             res = re.sub(' +', ' ', word)
#             if " " in res:
#                 word_list = res.split()
#                 for w in word_list:
#                     words.append(w)
#                     continue
#             if word.isnumeric():
#                 word = int(word)
#             tokens_list.append(word)
#         # tokens.extend(tokens_list) # COMMENTED OUT FOR MEMORY!!!
#     except FileNotFoundError:
#         raise FileNotFoundError("File Not Found.")
#     except UnicodeDecodeError:
#         raise UnicodeDecodeError("Unable to decode file due to encoding issues.")
#     except PermissionError:
#         raise PermissionError("Permission denied.")
#     except Exception as e:
#         raise Exception(f"An unexpected error occurred: {e}")
#     return tokens_list

# def computeWordFrequencies(list_token: list) -> dict:
#     list_token_copy = tokens[:]
#     token_map = {}
#     for word in list_token_copy:
#         if word not in list(token_map.keys()):
#             token_map[word] = list_token.count(word)
#             list_token_copy = [x for x in list_token_copy if x != word]
#     token_map_copy = token_map.copy()
#     del token_map[""] # should remove spaces that come up as tokens
#     with open("stop_words.txt") as file:
#         contents = file.readlines()
#         for keyword in contents:
#             if keyword in token_map_copy:
#                 del token_map[keyword]
#     token_map = {k: v for k, v in sorted(token_map.items(), key=lambda x: x[1])}
#     return token_map[:50]

def tokenize(text):
    """
    Tokenizes the given text string.
    Parameters:
    text (str): The text string to be tokenized.
    Returns:
    list: A list of tokens (words) extracted from the text string.
    Time Complexity: O(n), where n is the number of characters in the text string.
    """
    tokens = []
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

