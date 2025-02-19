import hashlib

# hard code things to avoid
# unique pages and filtered

def checksum(tokens:list):
    """
    Calculates the checksum of a list of tokens using MD5. Order of tokens not considered.
    @param: list of tokens (string)
    @return: integer value of checksum
    """
    hashed_toks = [int(hashlib.md5(token.encode('utf-8')).hexdigest(), 16) for token in tokens]
    return sum(hashed_toks)


def simhash(tok_weights:dict):
    """
    Calculates the 64 bit simhash given a dictionary of token: frequency using MD5.

    @param: dictionary of token: frequency
    @return: integer representation of 64 bit simhash of the tokens
    """
    hash_values = [0] * 64
    for token in tok_weights.keys():
        hash_val = bin(int.from_bytes(hashlib.md5(token.encode('utf-8')).digest(), byteorder='big'))[2:66] # bit string
        for i in range(64):
            if hash_val[i] == '0':
                hash_values[i] -= tok_weights[token]
            else:
                hash_values[i] += tok_weights[token]
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
    tokens15 = ["Deeksha", "Hello", "and", "Pragya"]
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
    print(checksum(tokens1))
    print(checksum(tokens15))
    print(checksum(tokens2))
