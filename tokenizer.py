import contractions
import re

# have a file of stop words

def tokenize(content: str) -> list:
    """
	Takes a string of content, returns a list of viable tokens in the string.
	
	@param content: string of content.
	@return: list of nonunique tokens
	"""
    tokens_list = []
    try:
		# words = contractions.fix(content.lower()).split()
        words = content.lower().split()
        for word in words:
            if '-' in word:
                word_separate = word.split('-')
                words.append(str(word_separate))
                continue
            word = re.sub(r'[^a-z0-9]', " ", word)
            res = re.sub(' +', ' ', word)
            if " " in res:
                word_list = res.split()
                for w in word_list:
                    words.append(w)
                    continue
            if word.isnumeric():
                word = int(word)
            tokens_list.append(word)
        return tokens_list
    except FileNotFoundError:
        raise FileNotFoundError("File Not Found.")
    except UnicodeDecodeError:
        raise UnicodeDecodeError("Unable to decode file due to encoding issues.")
    except PermissionError:
        raise PermissionError("Permission denied.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")

def computeWordFrequencies(list_token: list) -> dict:
    list_token_copy = list_token[:]
    token_map = {}
    for word in list_token_copy:
        if word not in list(token_map.keys()):
            token_map[word] = list_token.count(word)
            list_token_copy = [x for x in list_token_copy if x != word]
    token_map_copy = token_map.copy()
    with open("stop_words.txt") as file:
        contents = file.readlines()
        for keyword in contents:
            if keyword in token_map_copy:
                del token_map[keyword]
    return token_map