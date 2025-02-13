import hashlib

# hard code things to avoid
# unique pages and filtered

def get_frequencies(tokens:list):
    """
    Get the frequencies of each tokens to use as weights.

    @param: list of tokens
    @return: diction of token to frequency
    """
    freq = {}
    for token in tokens:
        if token in freq.keys():
            freq[token] += 1
        else:
            freq[token] = 1
    return freq


def simhash(tokens:list):
    """
    Calculates the 64 bit simhash given a list of tokens using MD5.

    @param: list of tokens
    @return: integer representation of 64 bit simhash of the tokens
    """
    weights = get_frequencies(tokens)
    hash_values = [0] * 64
    for token in weights.keys():
        hash_val = bin(int.from_bytes(hashlib.md5(token.encode('utf-8')).digest()))[2:66] # bit string
        for i in range(64):
            if hash_val[i] == '0':
                hash_values[i] -= weights[token]
            else:
                hash_values[i] += weights[token]
    simhash_val = ["0" if bit <= 0 else "1" for bit in hash_values]
    return bitvector_to_int(simhash_val)


def bitvector_to_int(simhash_val:list):
    """
    Given a list of simhash bits (bitvector of 64), converts the binary to an integer.
    @param: list of simhash value or bitvector, length is 64
    @return: integer equivalent to simhash bitvector
    """
    bin_str = "0b" + "".join(simhash_val)
    return int(bin_str, 2)


def similarity_score(sim1:int, sim2:int):
    """
    Given 2 simhash values in integer representation, calculate their similarity using XOR and NOT.
    @param: sim1 simhash value in integer, sim2 simhash value in integer
    @return: similarity score between 0 and 1 in float of similar bits / total num of bits
    """
    diff_bits = sim1 ^ sim2
    same_bits = (~diff_bits) & ((1 << 64) - 1)
    same_count = 0
    while same_bits:
        same_count += 1
        same_bits &= same_bits - 1 # thank you algonotes, and Deeksha, for this fancy while loop!
    return same_count / 64


if __name__ == "__main__":
    tokens1 = ["Hello", "Deeksha", "and", "Pragya"]
    tokens2 = ["Hello", "Deeksha", "and", "Pragya", "and", "Helena"]
    tokens3 = ["Bye", "for", "now", "hahahaha", "more", "tokens"]
    sim1 = simhash(tokens1)
    sim2 = simhash(tokens2)
    sim3 = simhash(tokens3)
    print(sim1)
    print(sim2)
    print(sim3)
    print(similarity_score(sim1, sim2))
    print(similarity_score(sim1, sim3))
    print(similarity_score(sim2, sim3))
